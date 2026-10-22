--!strict
-- Thin wrapper over AnalyticsService. Analytics must never break gameplay, so every call is pcall'd.
-- Events appear in Creator Hub > Analytics (custom events, funnels, economy).

local AnalyticsService = game:GetService("AnalyticsService")

local Analytics = {}

function Analytics.Custom(player: Player, eventName: string, value: number?)
	local ok, err = pcall(function()
		AnalyticsService:LogCustomEvent(player, eventName, value or 1)
	end)
	if not ok then
		warn(`[Analytics] {eventName}: {err}`)
	end
end

-- Records Cash entering the economy from gameplay (reports, survived nights).
function Analytics.CashEarned(player: Player, amount: number, endingBalance: number, source: string)
	local ok, err = pcall(function()
		AnalyticsService:LogEconomyEvent(
			player,
			Enum.AnalyticsEconomyFlowType.Source,
			"Cash",
			amount,
			endingBalance,
			Enum.AnalyticsEconomyTransactionType.Gameplay.Name,
			source
		)
	end)
	if not ok then
		warn(`[Analytics] CashEarned: {err}`)
	end
end

return Analytics
