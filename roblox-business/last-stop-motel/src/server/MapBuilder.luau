--!strict
-- Builds the greybox motel from code so the prototype runs in an empty place.
-- Every part that can host an anomaly gets the "AnomalyProp" tag and a unique PropId
-- attribute. Later the greybox can be replaced by a hand-built map that uses the same
-- tags and PropIds, and nothing else has to change.

local CollectionService = game:GetService("CollectionService")
local Lighting = game:GetService("Lighting")

local MapBuilder = {}

export type PartSpec = {
	Name: string,
	Size: Vector3,
	CFrame: CFrame,
	Color: Color3?,
	Material: Enum.Material?,
	CanCollide: boolean?,
	PropId: string?,
}

local WALL_COLOR = Color3.fromRGB(120, 110, 95)
local FLOOR_COLOR = Color3.fromRGB(70, 60, 50)
local CEILING_COLOR = Color3.fromRGB(90, 85, 80)
local WARM_LIGHT = Color3.fromRGB(255, 214, 160)

-- Yaw that makes a part's Front face (-Z) point along the given world direction.
local FACE_PLUS_X = CFrame.Angles(0, -math.pi / 2, 0)
local FACE_MINUS_X = CFrame.Angles(0, math.pi / 2, 0)
local FACE_PLUS_Z = CFrame.Angles(0, math.pi, 0)

local function makePart(spec: PartSpec, parent: Instance): Part
	local part = Instance.new("Part")
	part.Name = spec.Name
	part.Size = spec.Size
	part.CFrame = spec.CFrame
	part.Color = spec.Color or WALL_COLOR
	part.Material = spec.Material or Enum.Material.SmoothPlastic
	part.CanCollide = if spec.CanCollide == nil then true else spec.CanCollide
	part.Anchored = true
	part.TopSurface = Enum.SurfaceType.Smooth
	part.BottomSurface = Enum.SurfaceType.Smooth
	if spec.PropId then
		part:SetAttribute("PropId", spec.PropId)
		CollectionService:AddTag(part, "AnomalyProp")
	end
	part.Parent = parent
	return part
end

local function addText(part: BasePart, text: string, textColor: Color3, background: Color3)
	local gui = Instance.new("SurfaceGui")
	gui.Name = "Display"
	gui.Face = Enum.NormalId.Front
	gui.SizingMode = Enum.SurfaceGuiSizingMode.PixelsPerStud
	gui.PixelsPerStud = 50
	gui.LightInfluence = 0.3

	local label = Instance.new("TextLabel")
	label.Name = "Label"
	label.Size = UDim2.fromScale(1, 1)
	label.BackgroundColor3 = background
	label.TextColor3 = textColor
	label.TextScaled = true
	label.Font = Enum.Font.GothamBold
	label.Text = text
	label.Parent = gui

	gui.Parent = part
end

local function addLight(part: BasePart, color: Color3, range: number, brightness: number)
	local light = Instance.new("PointLight")
	light.Color = color
	light.Range = range
	light.Brightness = brightness
	light.Shadows = true
	light.Parent = part
end

local function buildShell(parent: Instance)
	-- Lobby: x in [-20, 20], z in [-20, 20]. Hallway: x in [-6, 6], z in [-80, -20].
	local specs: { PartSpec } = {
		{ Name = "LobbyFloor", Size = Vector3.new(40, 1, 40), CFrame = CFrame.new(0, -0.5, 0), Color = FLOOR_COLOR, Material = Enum.Material.WoodPlanks },
		{ Name = "LobbyCeiling", Size = Vector3.new(42, 1, 42), CFrame = CFrame.new(0, 14.5, 0), Color = CEILING_COLOR },
		{ Name = "LobbyWallFront", Size = Vector3.new(42, 14, 1), CFrame = CFrame.new(0, 7, 20.5) },
		{ Name = "LobbyWallLeft", Size = Vector3.new(1, 14, 40), CFrame = CFrame.new(-20.5, 7, 0) },
		{ Name = "LobbyWallRight", Size = Vector3.new(1, 14, 40), CFrame = CFrame.new(20.5, 7, 0) },
		{ Name = "LobbyWallBackLeft", Size = Vector3.new(15, 14, 1), CFrame = CFrame.new(-13.5, 7, -20.5) },
		{ Name = "LobbyWallBackRight", Size = Vector3.new(15, 14, 1), CFrame = CFrame.new(13.5, 7, -20.5) },
		{ Name = "HallFloor", Size = Vector3.new(12, 1, 60), CFrame = CFrame.new(0, -0.5, -50), Color = Color3.fromRGB(60, 45, 45), Material = Enum.Material.Fabric },
		{ Name = "HallCeiling", Size = Vector3.new(14, 1, 61), CFrame = CFrame.new(0, 14.5, -50.5), Color = CEILING_COLOR },
		{ Name = "HallWallLeft", Size = Vector3.new(1, 14, 60), CFrame = CFrame.new(-6.5, 7, -50) },
		{ Name = "HallWallRight", Size = Vector3.new(1, 14, 60), CFrame = CFrame.new(6.5, 7, -50) },
		{ Name = "HallWallEnd", Size = Vector3.new(14, 14, 1), CFrame = CFrame.new(0, 7, -80.5) },
		{ Name = "FrontDesk", Size = Vector3.new(14, 4, 3), CFrame = CFrame.new(0, 2, 8), Color = Color3.fromRGB(95, 60, 35), Material = Enum.Material.Wood },
		{ Name = "LobbyCeilingLamp", Size = Vector3.new(3, 0.5, 3), CFrame = CFrame.new(0, 13.75, 0), Color = WARM_LIGHT, Material = Enum.Material.Neon },
	}
	for _, spec in specs do
		local part = makePart(spec, parent)
		if spec.Name == "LobbyCeilingLamp" then
			addLight(part, WARM_LIGHT, 40, 1.2)
		end
	end

	local spawn = Instance.new("SpawnLocation")
	spawn.Name = "ShiftSpawn"
	spawn.Size = Vector3.new(6, 0.2, 6)
	spawn.CFrame = CFrame.new(0, 0.1, 14)
	spawn.Anchored = true
	spawn.Neutral = true
	spawn.Transparency = 1
	spawn.CanCollide = false
	spawn.Duration = 0
	spawn.Parent = parent
end

local function buildProps(parent: Instance)
	-- Lobby
	local painting = makePart({
		Name = "LobbyPainting",
		PropId = "LobbyPainting",
		Size = Vector3.new(8, 5, 0.4),
		CFrame = CFrame.new(-8, 8, 19.7),
		Color = Color3.fromRGB(40, 30, 25),
	}, parent)
	addText(painting, "Welcome to the Last Stop", Color3.fromRGB(240, 220, 180), Color3.fromRGB(45, 70, 60))

	local vacancy = makePart({
		Name = "VacancySign",
		PropId = "VacancySign",
		Size = Vector3.new(7, 2, 0.3),
		CFrame = CFrame.new(10, 10, 19.8),
		CanCollide = false,
	}, parent)
	addText(vacancy, "NO VACANCY", Color3.fromRGB(255, 80, 80), Color3.fromRGB(20, 10, 10))

	local deskLamp = makePart({
		Name = "DeskLamp",
		PropId = "DeskLamp",
		Size = Vector3.new(1, 1.5, 1),
		CFrame = CFrame.new(5, 4.75, 8),
		Color = WARM_LIGHT,
		Material = Enum.Material.Neon,
	}, parent)
	addLight(deskLamp, WARM_LIGHT, 18, 1.5)

	makePart({ Name = "LobbyPlant", PropId = "LobbyPlant", Size = Vector3.new(2, 5, 2), CFrame = CFrame.new(16, 2.5, 16), Color = Color3.fromRGB(50, 120, 60), Material = Enum.Material.Grass }, parent)
	makePart({ Name = "Chair1", PropId = "Chair1", Size = Vector3.new(3, 3, 3), CFrame = CFrame.new(-15, 1.5, -6), Color = Color3.fromRGB(50, 70, 130), Material = Enum.Material.Fabric }, parent)
	makePart({ Name = "Chair2", PropId = "Chair2", Size = Vector3.new(3, 3, 3), CFrame = CFrame.new(-10, 1.5, -6), Color = Color3.fromRGB(50, 70, 130), Material = Enum.Material.Fabric }, parent)
	makePart({ Name = "VendingMachine", PropId = "VendingMachine", Size = Vector3.new(4, 7, 3), CFrame = CFrame.new(16, 3.5, -15), Color = Color3.fromRGB(170, 30, 30) }, parent)
	makePart({ Name = "FireExtinguisher", PropId = "FireExtinguisher", Size = Vector3.new(1, 3, 1), CFrame = CFrame.new(-19.4, 2, 12), Color = Color3.fromRGB(200, 20, 20), Material = Enum.Material.Metal }, parent)
	makePart({ Name = "LobbyRug", PropId = "LobbyRug", Size = Vector3.new(12, 0.1, 8), CFrame = CFrame.new(0, 0.05, -6), Color = Color3.fromRGB(110, 30, 35), Material = Enum.Material.Fabric, CanCollide = false }, parent)

	-- Hallway doors: right wall faces -X, left wall faces +X
	local doors = {
		{ Number = "101", Position = Vector3.new(6, 4, -30), Facing = FACE_MINUS_X },
		{ Number = "102", Position = Vector3.new(-6, 4, -30), Facing = FACE_PLUS_X },
		{ Number = "103", Position = Vector3.new(6, 4, -55), Facing = FACE_MINUS_X },
		{ Number = "104", Position = Vector3.new(-6, 4, -55), Facing = FACE_PLUS_X },
	}
	for _, door in doors do
		-- Doors sit 0.25 studs out from the wall surface toward the hall center
		local inset = if door.Position.X > 0 then -0.25 else 0.25
		local base = CFrame.new(door.Position + Vector3.new(inset, 0, 0)) * door.Facing
		makePart({
			Name = "Door" .. door.Number,
			PropId = "Door" .. door.Number,
			Size = Vector3.new(4, 8, 0.4),
			CFrame = base,
			Color = Color3.fromRGB(110, 75, 45),
			Material = Enum.Material.Wood,
		}, parent)
		local sign = makePart({
			Name = "DoorSign" .. door.Number,
			PropId = "DoorSign" .. door.Number,
			Size = Vector3.new(2, 1, 0.2),
			CFrame = base * CFrame.new(0, 5, 0),
			CanCollide = false,
		}, parent)
		addText(sign, door.Number, Color3.fromRGB(230, 200, 120), Color3.fromRGB(30, 25, 20))
	end

	local hallPainting = makePart({
		Name = "HallPainting",
		PropId = "HallPainting",
		Size = Vector3.new(6, 4, 0.4),
		CFrame = CFrame.new(-5.75, 7, -42.5) * FACE_PLUS_X,
		Color = Color3.fromRGB(40, 30, 25),
	}, parent)
	addText(hallPainting, "Sweet Dreams", Color3.fromRGB(250, 240, 220), Color3.fromRGB(60, 50, 90))

	local exitSign = makePart({
		Name = "ExitSign",
		PropId = "ExitSign",
		Size = Vector3.new(4, 1.5, 0.3),
		CFrame = CFrame.new(0, 11, -79.8) * FACE_PLUS_Z,
		CanCollide = false,
	}, parent)
	addText(exitSign, "EXIT", Color3.fromRGB(80, 255, 120), Color3.fromRGB(10, 30, 15))

	makePart({ Name = "IceMachine", PropId = "IceMachine", Size = Vector3.new(3, 6, 3), CFrame = CFrame.new(3.5, 3, -76), Color = Color3.fromRGB(200, 205, 210), Material = Enum.Material.Metal }, parent)

	for index, z in { -32, -48, -64 } do
		local lamp = makePart({
			Name = "HallLamp" .. index,
			PropId = "HallLamp" .. index,
			Size = Vector3.new(2, 0.5, 2),
			CFrame = CFrame.new(0, 13.75, z),
			Color = WARM_LIGHT,
			Material = Enum.Material.Neon,
		}, parent)
		addLight(lamp, WARM_LIGHT, 22, 1.2)
	end
end

local function setNightLighting()
	Lighting.ClockTime = 0
	Lighting.Brightness = 0.5
	Lighting.Ambient = Color3.fromRGB(35, 35, 45)
	Lighting.OutdoorAmbient = Color3.fromRGB(25, 25, 35)
	Lighting.EnvironmentDiffuseScale = 0.2
	Lighting.EnvironmentSpecularScale = 0.2
end

function MapBuilder.Build(): Folder
	local existing = workspace:FindFirstChild("Motel")
	if existing then
		-- A hand-built map is already in the place; use it as-is.
		return existing :: Folder
	end

	local folder = Instance.new("Folder")
	folder.Name = "Motel"
	buildShell(folder)
	buildProps(folder)
	folder.Parent = workspace

	setNightLighting()
	return folder
end

return MapBuilder
