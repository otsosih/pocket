--!strict
-- Server entry point. Order matters: the map must exist before the director scans it.

local MapBuilder = require(script.MapBuilder)
local DataService = require(script.DataService)
local ShiftService = require(script.ShiftService)

MapBuilder.Build()
DataService.Init()
ShiftService.Start()
