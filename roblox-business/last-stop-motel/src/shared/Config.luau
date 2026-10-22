--!strict
-- Tuning values shared by server and client. Change numbers here, not in the systems.

local Config = {
	-- Night timing
	NIGHT_DURATION_SECONDS = 360, -- 6 in-game hours (00:00 -> 06:00), 1 real minute per hour
	INTERMISSION_SECONDS = 20, -- time to study the "normal" motel between nights
	FIRST_ANOMALY_DELAY = 15,
	SPAWN_INTERVAL_START = 35, -- seconds between anomalies at the start of the night
	SPAWN_INTERVAL_END = 15, -- ... and near dawn

	-- Lose conditions
	MAX_ACTIVE_ANOMALIES = 4, -- this many unreported anomalies at once = night lost
	MAX_STRIKES = 3, -- this many false reports = night lost

	-- Reporting
	REPORT_COOLDOWN = 2, -- seconds between reports per player
	REPORT_HOLD_DURATION = 0.75,
	REPORT_DISTANCE = 14,

	-- Rewards (soft currency "Cash")
	REWARD_CORRECT_REPORT = 10,
	REWARD_NIGHT_SURVIVED = 50,

	-- Shared object names
	STATE_FOLDER_NAME = "ShiftState",
	NOTIFY_REMOTE_NAME = "Notify",
}

return Config
