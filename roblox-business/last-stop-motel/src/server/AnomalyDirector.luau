--!strict
-- Server-authoritative anomaly state: picks, applies, resolves and clears anomalies,
-- and turns "hold E on a prop" into a report callback. Clients never decide anything.

local CollectionService = game:GetService("CollectionService")

local Config = require(game:GetService("ReplicatedStorage").Shared.Config)
local Definitions = require(script.Parent.AnomalyDefinitions)

type Definition = Definitions.Definition
type ActiveAnomaly = {
	Definition: Definition,
	Revert: () -> (),
}
export type ReportHandler = (player: Player, propId: string) -> ()

local AnomalyDirector = {}

local PROP_TAG = "AnomalyProp"

local propsById: { [string]: BasePart } = {}
local activeByProp: { [string]: ActiveAnomaly } = {}
local reportHandler: ReportHandler? = nil
local random = Random.new()

local function attachPrompt(part: BasePart)
	local propId = part:GetAttribute("PropId")
	if typeof(propId) ~= "string" then
		warn(`[AnomalyDirector] {part:GetFullName()} is tagged but has no PropId`)
		return
	end

	-- Clones arrive with the prompt already inside; reuse it but connect fresh.
	local prompt = part:FindFirstChild("ReportPrompt") :: ProximityPrompt?
	if not prompt then
		local newPrompt = Instance.new("ProximityPrompt")
		newPrompt.Name = "ReportPrompt"
		newPrompt.ActionText = "Report anomaly"
		newPrompt.ObjectText = ""
		newPrompt.HoldDuration = Config.REPORT_HOLD_DURATION
		newPrompt.MaxActivationDistance = Config.REPORT_DISTANCE
		newPrompt.RequiresLineOfSight = false
		newPrompt.Parent = part
		prompt = newPrompt
	end
	assert(prompt, "prompt was just created")

	prompt.Triggered:Connect(function(player: Player)
		if reportHandler then
			reportHandler(player, propId)
		end
	end)
end

function AnomalyDirector.Init(onReport: ReportHandler)
	reportHandler = onReport

	for _, instance in CollectionService:GetTagged(PROP_TAG) do
		if instance:IsA("BasePart") then
			local propId = instance:GetAttribute("PropId")
			if typeof(propId) == "string" then
				propsById[propId] = instance
			end
			attachPrompt(instance)
		end
	end

	-- Duplicated props (e.g. "extra chair") get their own working prompt.
	CollectionService:GetInstanceAddedSignal(PROP_TAG):Connect(function(instance: Instance)
		if instance:IsA("BasePart") then
			attachPrompt(instance)
		end
	end)

	-- Catch typos in the catalogue at startup instead of mid-night.
	for _, definition in Definitions do
		if not propsById[definition.PropId] then
			warn(`[AnomalyDirector] Anomaly "{definition.Id}" targets missing prop "{definition.PropId}"`)
		end
	end
end

-- Spawns one random anomaly on a prop that is currently normal. Returns it, or nil if none fit.
function AnomalyDirector.SpawnRandom(): Definition?
	local candidates: { Definition } = {}
	local totalWeight = 0
	for _, definition in Definitions do
		if propsById[definition.PropId] and not activeByProp[definition.PropId] then
			table.insert(candidates, definition)
			totalWeight += definition.Weight
		end
	end
	if #candidates == 0 then
		return nil
	end

	local roll = random:NextNumber() * totalWeight
	local chosen = candidates[#candidates]
	for _, definition in candidates do
		roll -= definition.Weight
		if roll <= 0 then
			chosen = definition
			break
		end
	end

	local revert = chosen.Apply(propsById[chosen.PropId])
	activeByProp[chosen.PropId] = { Definition = chosen, Revert = revert }
	return chosen
end

-- Resolves the anomaly on this prop if there is one. Returns its definition, or nil (false report).
function AnomalyDirector.Resolve(propId: string): Definition?
	local active = activeByProp[propId]
	if not active then
		return nil
	end
	activeByProp[propId] = nil
	active.Revert()
	return active.Definition
end

function AnomalyDirector.ActiveCount(): number
	local count = 0
	for _ in activeByProp do
		count += 1
	end
	return count
end

function AnomalyDirector.ClearAll()
	for propId, active in activeByProp do
		activeByProp[propId] = nil
		active.Revert()
	end
end

return AnomalyDirector
