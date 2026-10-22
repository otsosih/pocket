--!strict
-- The night-shift loop: intermission -> night (anomalies spawn, players report) -> result.
-- Owns strikes, rewards and the replicated shift state that the client HUD reads.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Config = require(ReplicatedStorage.Shared.Config)
local AnomalyDirector = require(script.Parent.AnomalyDirector)
local DataService = require(script.Parent.DataService)
local Analytics = require(script.Parent.Analytics)

local ShiftService = {}

type Phase = "Waiting" | "Intermission" | "Night"

local state: Folder
local notify: RemoteEvent

local phase: Phase = "Waiting"
local strikes = 0
local nightNumber = 0
local lastReportAt: { [Player]: number } = {}

local function setState(name: string, value: any)
	state:SetAttribute(name, value)
end

local function broadcast(message: string, kind: string)
	notify:FireAllClients(message, kind)
end

-- "00:00 AM" .. "06:00 AM" from seconds elapsed in the night.
local function clockText(elapsed: number): string
	local hoursPerSecond = 6 / Config.NIGHT_DURATION_SECONDS
	local totalMinutes = math.floor(elapsed * hoursPerSecond * 60)
	local hours = math.clamp(math.floor(totalMinutes / 60), 0, 6)
	local minutes = if hours >= 6 then 0 else totalMinutes % 60
	local displayHour = if hours == 0 then 12 else hours
	return string.format("%02d:%02d AM", displayHour, minutes)
end

local function spawnInterval(elapsed: number): number
	local progress = math.clamp(elapsed / Config.NIGHT_DURATION_SECONDS, 0, 1)
	return Config.SPAWN_INTERVAL_START + (Config.SPAWN_INTERVAL_END - Config.SPAWN_INTERVAL_START) * progress
end

local function reward(player: Player, amount: number, source: string)
	if DataService.AddCash(player, amount) then
		local data = DataService.Get(player)
		Analytics.CashEarned(player, amount, if data then data.Cash else 0, source)
	end
end

local function onReport(player: Player, propId: string)
	if phase ~= "Night" then
		return
	end
	local now = os.clock()
	if now - (lastReportAt[player] or 0) < Config.REPORT_COOLDOWN then
		return
	end
	lastReportAt[player] = now

	local resolved = AnomalyDirector.Resolve(propId)
	if resolved then
		reward(player, Config.REWARD_CORRECT_REPORT, "CorrectReport")
		local isNew = DataService.DiscoverAnomaly(player, resolved.Id)
		local suffix = if isNew then "  (NEW in your journal!)" else ""
		broadcast(`{player.DisplayName} reported: {resolved.Name}{suffix}`, "good")
		Analytics.Custom(player, "AnomalyReported")
	else
		strikes += 1
		setState("Strikes", strikes)
		broadcast(`False report by {player.DisplayName}! Strike {strikes}/{Config.MAX_STRIKES}`, "bad")
		Analytics.Custom(player, "FalseReport")
	end
end

local function runIntermission()
	phase = "Intermission"
	setState("Phase", phase)
	setState("ClockText", "Get ready")
	for remaining = Config.INTERMISSION_SECONDS, 1, -1 do
		setState("Countdown", remaining)
		if remaining == Config.INTERMISSION_SECONDS then
			broadcast("Memorise the motel. Anything that changes tonight is an anomaly.", "info")
		end
		task.wait(1)
	end
	setState("Countdown", 0)
end

-- Returns true if the players survived until 6 AM.
local function runNight(): boolean
	nightNumber += 1
	strikes = 0
	phase = "Night"
	setState("Phase", phase)
	setState("Strikes", 0)
	setState("NightNumber", nightNumber)
	broadcast(`Night {nightNumber} begins. Hold E on anything that is wrong.`, "info")
	for _, player in Players:GetPlayers() do
		Analytics.Custom(player, "NightStarted", nightNumber)
	end

	local startedAt = os.clock()
	local nextSpawnAt = Config.FIRST_ANOMALY_DELAY
	while true do
		local elapsed = os.clock() - startedAt
		setState("ClockText", clockText(elapsed))

		if elapsed >= Config.NIGHT_DURATION_SECONDS then
			return true
		end
		if #Players:GetPlayers() == 0 then
			return false
		end
		if strikes >= Config.MAX_STRIKES then
			broadcast("Too many false reports. The manager fired you...", "bad")
			return false
		end
		if AnomalyDirector.ActiveCount() >= Config.MAX_ACTIVE_ANOMALIES then
			broadcast("Too many anomalies went unnoticed. They got in...", "bad")
			return false
		end

		if elapsed >= nextSpawnAt then
			AnomalyDirector.SpawnRandom()
			nextSpawnAt = elapsed + spawnInterval(elapsed)
		end
		task.wait(0.5)
	end
end

local function finishNight(survived: boolean)
	AnomalyDirector.ClearAll()
	for _, player in Players:GetPlayers() do
		if survived then
			reward(player, Config.REWARD_NIGHT_SURVIVED, "NightSurvived")
			DataService.RecordNightSurvived(player)
		end
		Analytics.Custom(player, if survived then "NightWon" else "NightLost", nightNumber)
	end
	if survived then
		broadcast(`6:00 AM. You survived night {nightNumber}! +{Config.REWARD_NIGHT_SURVIVED} Cash`, "good")
	end
	task.wait(4)
end

function ShiftService.Start()
	state = Instance.new("Folder")
	state.Name = Config.STATE_FOLDER_NAME
	state:SetAttribute("Phase", phase)
	state:SetAttribute("ClockText", "Waiting for players")
	state:SetAttribute("Strikes", 0)
	state:SetAttribute("MaxStrikes", Config.MAX_STRIKES)
	state:SetAttribute("Countdown", 0)
	state:SetAttribute("NightNumber", 0)
	state.Parent = ReplicatedStorage

	notify = Instance.new("RemoteEvent")
	notify.Name = Config.NOTIFY_REMOTE_NAME
	notify.Parent = ReplicatedStorage

	AnomalyDirector.Init(onReport)
	Players.PlayerRemoving:Connect(function(player)
		lastReportAt[player] = nil
	end)

	task.spawn(function()
		while true do
			if #Players:GetPlayers() == 0 then
				phase = "Waiting"
				setState("Phase", phase)
				setState("ClockText", "Waiting for players")
				Players.PlayerAdded:Wait()
			end
			runIntermission()
			finishNight(runNight())
		end
	end)
end

return ShiftService
