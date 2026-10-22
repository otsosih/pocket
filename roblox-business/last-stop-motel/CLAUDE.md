# Last Stop Motel: conventions for AI-assisted development

- Luau, `--!strict` in every file. Rojo layout from `default.project.json`.
- Server-authoritative: the client only displays state. Rewards, anomaly state, purchases and saves live on the server.
- Content is data: new anomalies go in `src/server/AnomalyDefinitions.luau` and reuse `AnomalyEffects`. Anomaly `Id`s are saved in player journals, so never rename or reuse them.
- Props are found by the CollectionService tag `AnomalyProp` plus a unique `PropId` attribute, never by path.
- Balance numbers live only in `src/shared/Config.luau`.
- DataStore writes use `UpdateAsync` through `DataService` only. Never save data that failed to load.
- Wrap analytics and other non-critical service calls in `pcall`.
- Before committing, run: `luau-compile --null` on changed files, `luau-lsp analyze` with Roblox definitions, then `rojo build`.
- Never claim Studio behaviour was tested unless the founder ran it.
