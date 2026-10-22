--!strict
-- Reusable building blocks for anomalies. Each effect factory returns an Apply function:
-- Apply(prop) changes the prop and returns a Revert function that restores it exactly.

local AnomalyEffects = {}

export type Revert = () -> ()
export type Apply = (prop: BasePart) -> Revert

local function getLabel(prop: BasePart): TextLabel?
	local gui = prop:FindFirstChild("Display")
	if not gui then
		return nil
	end
	return gui:FindFirstChild("Label") :: TextLabel?
end

function AnomalyEffects.Move(offset: Vector3): Apply
	return function(prop)
		local original = prop.CFrame
		prop.CFrame = original + offset
		return function()
			prop.CFrame = original
		end
	end
end

function AnomalyEffects.Rotate(rotation: CFrame): Apply
	return function(prop)
		local original = prop.CFrame
		prop.CFrame = original * rotation
		return function()
			prop.CFrame = original
		end
	end
end

-- Swings a door-like part around its edge at local +X.
function AnomalyEffects.SwingOpen(angle: number): Apply
	return function(prop)
		local original = prop.CFrame
		local hinge = CFrame.new(prop.Size.X / 2, 0, 0)
		prop.CFrame = original * hinge * CFrame.Angles(0, angle, 0) * hinge:Inverse()
		return function()
			prop.CFrame = original
		end
	end
end

function AnomalyEffects.Recolor(color: Color3): Apply
	return function(prop)
		local original = prop.Color
		prop.Color = color
		return function()
			prop.Color = original
		end
	end
end

-- Scales the part while keeping its bottom on the same height.
function AnomalyEffects.Scale(factor: number): Apply
	return function(prop)
		local originalSize = prop.Size
		local originalCFrame = prop.CFrame
		local newSize = originalSize * factor
		prop.Size = newSize
		prop.CFrame = originalCFrame + Vector3.new(0, (newSize.Y - originalSize.Y) / 2, 0)
		return function()
			prop.Size = originalSize
			prop.CFrame = originalCFrame
		end
	end
end

function AnomalyEffects.Hide(): Apply
	return function(prop)
		local transparency = prop.Transparency
		local canCollide = prop.CanCollide
		local hiddenGuis: { SurfaceGui } = {}
		local hiddenLights: { Light } = {}
		prop.Transparency = 1
		prop.CanCollide = false
		for _, child in prop:GetChildren() do
			if child:IsA("SurfaceGui") and child.Enabled then
				child.Enabled = false
				table.insert(hiddenGuis, child)
			elseif child:IsA("Light") and child.Enabled then
				child.Enabled = false
				table.insert(hiddenLights, child)
			end
		end
		return function()
			prop.Transparency = transparency
			prop.CanCollide = canCollide
			for _, gui in hiddenGuis do
				gui.Enabled = true
			end
			for _, light in hiddenLights do
				light.Enabled = true
			end
		end
	end
end

-- Places a copy of the prop. The copy keeps the AnomalyProp tag and PropId,
-- so reporting either the original or the copy resolves the anomaly.
function AnomalyEffects.Duplicate(offset: Vector3): Apply
	return function(prop)
		local copy = prop:Clone()
		copy.CFrame = prop.CFrame + offset
		copy.Parent = prop.Parent
		return function()
			copy:Destroy()
		end
	end
end

function AnomalyEffects.LightColor(color: Color3): Apply
	return function(prop)
		local light = prop:FindFirstChildWhichIsA("PointLight")
		local originalPartColor = prop.Color
		local originalLightColor = if light then light.Color else nil
		prop.Color = color
		if light then
			light.Color = color
		end
		return function()
			prop.Color = originalPartColor
			if light and originalLightColor then
				light.Color = originalLightColor
			end
		end
	end
end

function AnomalyEffects.LightOff(): Apply
	return function(prop)
		local light = prop:FindFirstChildWhichIsA("PointLight")
		local originalMaterial = prop.Material
		local originalColor = prop.Color
		prop.Material = Enum.Material.SmoothPlastic
		prop.Color = Color3.fromRGB(40, 40, 40)
		if light then
			light.Enabled = false
		end
		return function()
			prop.Material = originalMaterial
			prop.Color = originalColor
			if light then
				light.Enabled = true
			end
		end
	end
end

function AnomalyEffects.SetText(text: string, textColor: Color3?): Apply
	return function(prop)
		local label = getLabel(prop)
		if not label then
			warn(`[AnomalyEffects] {prop:GetFullName()} has no Display.Label`)
			return function() end
		end
		local originalText = label.Text
		local originalColor = label.TextColor3
		label.Text = text
		if textColor then
			label.TextColor3 = textColor
		end
		return function()
			label.Text = originalText
			label.TextColor3 = originalColor
		end
	end
end

return AnomalyEffects
