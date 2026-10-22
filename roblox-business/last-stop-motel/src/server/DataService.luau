--!strict
-- Player save data with session locking, retries, autosave and safe shutdown.
--
-- Rules this module enforces:
--  * Data that failed to load is NEVER saved, so a DataStore outage can't wipe progress.
--  * A session lock stops two servers from writing the same player at once.
--  * Every write goes through UpdateAsync.

local DataStoreService = game:GetService("DataStoreService")
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")

local DataService = {}

export type PlayerData = {
	Version: number,
	Cash: number,
	NightsSurvived: number,
	Journal: { [string]: boolean }, -- anomaly Id -> discovered
}

type SessionLock = { JobId: string, Time: number }
type StoredRecord = { Data: PlayerData, Lock: SessionLock? }
type Profile = {
	Data: PlayerData,
	CanSave: boolean, -- false when loading failed; progress is kept in memory only
}

local STORE_NAME = "PlayerData_v1"
local DATA_VERSION = 1
local AUTOSAVE_INTERVAL = 120
local LOCK_EXPIRY_SECONDS = 1800 -- a lock older than this belongs to a crashed server
local LOAD_ATTEMPTS = 5
local RETRY_DELAY = 4

local store: DataStore? = nil
local profiles: { [Player]: Profile } = {}
local savingNow: { [Player]: boolean } = {}

local function defaultData(): PlayerData
	return { Version = DATA_VERSION, Cash = 0, NightsSurvived = 0, Journal = {} }
end

-- Fills fields added in later versions so old saves keep working.
local function reconcile(data: any): PlayerData
	local result = defaultData()
	if typeof(data) ~= "table" then
		return result
	end
	if typeof(data.Cash) == "number" then
		result.Cash = data.Cash
	end
	if typeof(data.NightsSurvived) == "number" then
		result.NightsSurvived = data.NightsSurvived
	end
	if typeof(data.Journal) == "table" then
		for id, discovered in data.Journal do
			if typeof(id) == "string" and discovered == true then
				result.Journal[id] = true
			end
		end
	end
	return result
end

local function keyFor(player: Player): string
	return `player_{player.UserId}`
end

local function lockIsForeign(lock: SessionLock?): boolean
	return lock ~= nil and lock.JobId ~= game.JobId and os.time() - lock.Time < LOCK_EXPIRY_SECONDS
end

local function setLeaderstat(player: Player, cash: number)
	local leaderstats = player:FindFirstChild("leaderstats")
	local value = leaderstats and leaderstats:FindFirstChild("Cash")
	if value and value:IsA("IntValue") then
		value.Value = cash
	end
end

local function loadAsync(player: Player): Profile
	local activeStore = store
	if not activeStore then
		return { Data = defaultData(), CanSave = false }
	end

	for attempt = 1, LOAD_ATTEMPTS do
		local blockedByLock = false
		local ok, result = pcall(function()
			return activeStore:UpdateAsync(keyFor(player), function(old: StoredRecord?): StoredRecord?
				if old and lockIsForeign(old.Lock) and attempt < LOAD_ATTEMPTS then
					blockedByLock = true
					return nil -- cancel the write; another server still owns this player
				end
				-- On the final attempt a stuck lock is taken over.
				return {
					Data = reconcile(old and old.Data),
					Lock = { JobId = game.JobId, Time = os.time() },
				}
			end)
		end)

		if ok and result and not blockedByLock then
			return { Data = reconcile((result :: StoredRecord).Data), CanSave = true }
		end
		if not ok then
			warn(`[DataService] Load attempt {attempt} failed for {player.Name}: {result}`)
			if string.find(tostring(result), "StudioAccessToApisNotAllowed", 1, true) then
				break -- retrying can't help; see the warning in Init
			end
		end
		if not player.Parent then
			break
		end
		task.wait(RETRY_DELAY)
	end

	warn(`[DataService] Could not load data for {player.Name}; progress will not be saved this session`)
	return { Data = defaultData(), CanSave = false }
end

local function saveAsync(player: Player, releaseLock: boolean): boolean
	local profile = profiles[player]
	local activeStore = store
	if not profile or not profile.CanSave or not activeStore then
		return false
	end
	if savingNow[player] then
		if not releaseLock then
			return false -- an autosave is already running
		end
		-- The final save must not be skipped: wait for the running one, then write again.
		while savingNow[player] do
			task.wait(0.1)
		end
	end
	savingNow[player] = true

	local data = profile.Data
	local ok, err = pcall(function()
		activeStore:UpdateAsync(keyFor(player), function(old: StoredRecord?): StoredRecord?
			if old and lockIsForeign(old.Lock) then
				return nil -- another server took over; don't overwrite its newer data
			end
			return {
				Data = data,
				Lock = if releaseLock then nil else { JobId = game.JobId, Time = os.time() },
			}
		end)
	end)
	savingNow[player] = nil

	if not ok then
		warn(`[DataService] Save failed for {player.Name}: {err}`)
	end
	return ok
end

local function onPlayerAdded(player: Player)
	local leaderstats = Instance.new("Folder")
	leaderstats.Name = "leaderstats"
	local cash = Instance.new("IntValue")
	cash.Name = "Cash"
	cash.Parent = leaderstats
	leaderstats.Parent = player

	local profile = loadAsync(player)
	if not player.Parent then
		-- Left while loading: hand the lock back immediately.
		if profile.CanSave then
			profiles[player] = profile
			saveAsync(player, true)
			profiles[player] = nil
		end
		return
	end
	profiles[player] = profile
	setLeaderstat(player, profile.Data.Cash)
end

local function onPlayerRemoving(player: Player)
	if profiles[player] then
		saveAsync(player, true)
		profiles[player] = nil
	end
end

function DataService.Init()
	local ok, result = pcall(function()
		return DataStoreService:GetDataStore(STORE_NAME)
	end)
	if ok then
		store = result
	else
		warn(`[DataService] DataStores unavailable ({result}). In Studio, enable Game Settings > Security > Studio Access to API Services.`)
	end

	Players.PlayerAdded:Connect(onPlayerAdded)
	Players.PlayerRemoving:Connect(onPlayerRemoving)
	for _, player in Players:GetPlayers() do
		task.spawn(onPlayerAdded, player)
	end

	task.spawn(function()
		while true do
			task.wait(AUTOSAVE_INTERVAL)
			for player in profiles do
				task.spawn(saveAsync, player, false)
			end
		end
	end)

	game:BindToClose(function()
		if RunService:IsStudio() and not store then
			return
		end
		local pending = 0
		for player in profiles do
			pending += 1
			task.spawn(function()
				saveAsync(player, true)
				pending -= 1
			end)
		end
		local deadline = os.clock() + 25
		while pending > 0 and os.clock() < deadline do
			task.wait(0.25)
		end
	end)
end

-- Read-only view for other systems. Returns nil until the player's data has loaded.
function DataService.Get(player: Player): PlayerData?
	local profile = profiles[player]
	return profile and profile.Data
end

function DataService.AddCash(player: Player, amount: number): boolean
	local profile = profiles[player]
	if not profile or amount ~= amount or amount < 0 then
		return false
	end
	profile.Data.Cash += math.floor(amount)
	setLeaderstat(player, profile.Data.Cash)
	return true
end

-- Returns true the first time a player discovers this anomaly.
function DataService.DiscoverAnomaly(player: Player, anomalyId: string): boolean
	local profile = profiles[player]
	if not profile or profile.Data.Journal[anomalyId] then
		return false
	end
	profile.Data.Journal[anomalyId] = true
	return true
end

function DataService.RecordNightSurvived(player: Player)
	local profile = profiles[player]
	if profile then
		profile.Data.NightsSurvived += 1
	end
end

return DataService
