--!strict
-- The anomaly catalogue. Adding content = adding an entry here.
-- Id must be unique and stable: it is saved in players' anomaly journals.

local Effects = require(script.Parent.AnomalyEffects)

export type Definition = {
	Id: string,
	Name: string, -- shown to players after the anomaly is reported
	PropId: string, -- which tagged prop it changes
	Weight: number, -- relative spawn chance
	Apply: Effects.Apply,
}

local RED = Color3.fromRGB(255, 40, 40)

local definitions: { Definition } = {
	{ Id = "painting_upside_down", Name = "Upside-down painting", PropId = "LobbyPainting", Weight = 1, Apply = Effects.Rotate(CFrame.Angles(0, 0, math.pi)) },
	{ Id = "painting_leave", Name = "The painting says LEAVE", PropId = "LobbyPainting", Weight = 0.7, Apply = Effects.SetText("LEAVE", RED) },
	{ Id = "vacancy_no_escape", Name = "NO ESCAPE sign", PropId = "VacancySign", Weight = 1, Apply = Effects.SetText("NO ESCAPE") },
	{ Id = "desk_lamp_red", Name = "Red desk lamp", PropId = "DeskLamp", Weight = 1, Apply = Effects.LightColor(RED) },
	{ Id = "plant_moved", Name = "Plant moved", PropId = "LobbyPlant", Weight = 1, Apply = Effects.Move(Vector3.new(-7, 0, 0)) },
	{ Id = "plant_missing", Name = "Missing plant", PropId = "LobbyPlant", Weight = 0.8, Apply = Effects.Hide() },
	{ Id = "chair_extra", Name = "Extra chair", PropId = "Chair1", Weight = 1, Apply = Effects.Duplicate(Vector3.new(-1, 0, 6)) },
	{ Id = "chair_giant", Name = "Giant chair", PropId = "Chair1", Weight = 0.8, Apply = Effects.Scale(1.8) },
	{ Id = "chair_turned", Name = "Chair turned to the wall", PropId = "Chair2", Weight = 1, Apply = Effects.Rotate(CFrame.Angles(0, math.rad(45), 0)) },
	{ Id = "vending_blue", Name = "Blue vending machine", PropId = "VendingMachine", Weight = 1, Apply = Effects.Recolor(Color3.fromRGB(30, 60, 170)) },
	{ Id = "vending_tall", Name = "Growing vending machine", PropId = "VendingMachine", Weight = 0.8, Apply = Effects.Scale(1.35) },
	{ Id = "extinguisher_missing", Name = "Missing fire extinguisher", PropId = "FireExtinguisher", Weight = 1, Apply = Effects.Hide() },
	{ Id = "rug_green", Name = "Green rug", PropId = "LobbyRug", Weight = 0.8, Apply = Effects.Recolor(Color3.fromRGB(30, 110, 50)) },
	{ Id = "door_102_open", Name = "Room 102 door open", PropId = "Door102", Weight = 1, Apply = Effects.SwingOpen(math.rad(-75)) },
	{ Id = "door_103_open", Name = "Room 103 door open", PropId = "Door103", Weight = 1, Apply = Effects.SwingOpen(math.rad(-75)) },
	{ Id = "door_sign_13", Name = "Room 13", PropId = "DoorSign104", Weight = 1, Apply = Effects.SetText("13") },
	{ Id = "door_sign_101_backwards", Name = "Room 101 sign upside down", PropId = "DoorSign101", Weight = 0.8, Apply = Effects.Rotate(CFrame.Angles(0, 0, math.pi)) },
	{ Id = "hall_painting_eyes", Name = "I SEE YOU painting", PropId = "HallPainting", Weight = 1, Apply = Effects.SetText("I SEE YOU", RED) },
	{ Id = "exit_no_exit", Name = "NO EXIT sign", PropId = "ExitSign", Weight = 1, Apply = Effects.SetText("NO EXIT", RED) },
	{ Id = "hall_lamp_off", Name = "Dead hallway lamp", PropId = "HallLamp2", Weight = 1, Apply = Effects.LightOff() },
	{ Id = "hall_lamp_red", Name = "Red hallway lamp", PropId = "HallLamp3", Weight = 1, Apply = Effects.LightColor(RED) },
	{ Id = "ice_machine_moved", Name = "Ice machine moved", PropId = "IceMachine", Weight = 1, Apply = Effects.Move(Vector3.new(-7, 0, 0)) },
}

return definitions
