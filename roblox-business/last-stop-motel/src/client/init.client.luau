--!strict
-- Client HUD: clock, strikes, countdown and toast messages. Display only, no game logic.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Config = require(ReplicatedStorage:WaitForChild("Shared"):WaitForChild("Config"))

local player = Players.LocalPlayer
local state = ReplicatedStorage:WaitForChild(Config.STATE_FOLDER_NAME)
local notify = ReplicatedStorage:WaitForChild(Config.NOTIFY_REMOTE_NAME) :: RemoteEvent

local TOAST_COLORS = {
	good = Color3.fromRGB(120, 255, 150),
	bad = Color3.fromRGB(255, 90, 90),
	info = Color3.fromRGB(240, 230, 210),
}

local gui = Instance.new("ScreenGui")
gui.Name = "ShiftHud"
gui.ResetOnSpawn = false
gui.IgnoreGuiInset = false
gui.Parent = player:WaitForChild("PlayerGui")

local function makeLabel(name: string, position: UDim2, size: UDim2, textSize: number): TextLabel
	local label = Instance.new("TextLabel")
	label.Name = name
	label.AnchorPoint = Vector2.new(0.5, 0)
	label.Position = position
	label.Size = size
	label.BackgroundColor3 = Color3.fromRGB(10, 10, 15)
	label.BackgroundTransparency = 0.35
	label.TextColor3 = Color3.fromRGB(240, 230, 210)
	label.Font = Enum.Font.GothamBold
	label.TextSize = textSize
	label.Text = ""
	local corner = Instance.new("UICorner")
	corner.CornerRadius = UDim.new(0, 8)
	corner.Parent = label
	label.Parent = gui
	return label
end

local clockLabel = makeLabel("Clock", UDim2.new(0.5, 0, 0, 8), UDim2.fromOffset(240, 44), 26)
local strikesLabel = makeLabel("Strikes", UDim2.new(0.5, 0, 0, 58), UDim2.fromOffset(240, 28), 18)
local toastLabel = makeLabel("Toast", UDim2.new(0.5, 0, 0.72, 0), UDim2.new(0.8, 0, 0, 48), 22)
toastLabel.TextWrapped = true
toastLabel.Visible = false

local function render()
	local phase = state:GetAttribute("Phase")
	local clock = state:GetAttribute("ClockText")
	local countdown = state:GetAttribute("Countdown")
	local strikes = state:GetAttribute("Strikes")
	local maxStrikes = state:GetAttribute("MaxStrikes")

	if phase == "Intermission" then
		clockLabel.Text = `Shift starts in {countdown}`
		strikesLabel.Visible = false
	elseif phase == "Night" then
		clockLabel.Text = `Night {state:GetAttribute("NightNumber")}  |  {clock}`
		strikesLabel.Visible = true
		strikesLabel.Text = `False reports: {strikes}/{maxStrikes}`
	else
		clockLabel.Text = tostring(clock)
		strikesLabel.Visible = false
	end
end

state.AttributeChanged:Connect(render)
render()

local toastToken = 0
notify.OnClientEvent:Connect(function(message: string, kind: string)
	toastToken += 1
	local token = toastToken
	toastLabel.Text = message
	toastLabel.TextColor3 = TOAST_COLORS[kind] or TOAST_COLORS.info
	toastLabel.TextTransparency = 0
	toastLabel.BackgroundTransparency = 0.35
	toastLabel.Visible = true

	task.delay(3.5, function()
		if token ~= toastToken then
			return -- a newer message replaced this one
		end
		local fade = TweenInfo.new(0.6)
		TweenService:Create(toastLabel, fade, { TextTransparency = 1, BackgroundTransparency = 1 }):Play()
	end)
end)
