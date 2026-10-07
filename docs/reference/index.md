# API reference

The types you are meant to use in TurnGauge, grouped by what they are for rather than by namespace. **423 types.**

!!! info "What is not listed here"
    74 further types are public in the source but left out of this reference. They are public only because `internal` is per-assembly in C# and the package spans several assemblies -- plumbing, not API. They carry `[EditorBrowsable(Never)]` in the source to say so. Nothing you need is hidden: if a documented type exposes it, it is documented too.

## Start here

The types a new project meets first.

| Type | Area | What it is for |
| --- | --- | --- |
| [`AdvanceTicksOutcome`](running-a-battle.md#advanceticksoutcome) | Running a battle | Why one `BattleEngine.AdvanceTicks(int)` call stopped. |
| [`AdvanceTicksResult`](running-a-battle.md#advanceticksresult) | Running a battle | Immutable result of one `BattleEngine.AdvanceTicks(int)` call: the outcome that stopped it, the absolute tick it was aiming for, every event emitted on the way in strict tick and e... |
| [`BattleEngine`](running-a-battle.md#battleengine) | Running a battle | Owns immutable battle state and advances it through deterministic command, scheduler, action, event, and mechanics reduction boundaries. |
| [`BattleResultState`](running-a-battle.md#battleresultstate) | Running a battle | The battle's outcome as of one snapshot: either nonterminal (`None`) or a terminal verdict naming the result and, for team outcomes, the surviving and eliminated teams. |
| [`BattleStartRequest`](running-a-battle.md#battlestartrequest) | Running a battle | The immutable opening state of one battle: the scheduler that will run it, the two opposing teams, and the health, resources, and statuses every combatant starts with. |
| [`BattleCommand`](commands-events-and-snapshots.md#battlecommand) | Commands, events and snapshots | One immutable decision handed to a battle: which combatant acts, on which tick, under which command type, and against what. |
| [`BattleEvent`](commands-events-and-snapshots.md#battleevent) | Commands, events and snapshots | One immutable gameplay event emitted by the battle engine: what happened, on which tick, in what order, and under which root action. |
| [`BattleIds`](commands-events-and-snapshots.md#battleids) | Commands, events and snapshots | The stable identifiers the battle simulation emits and reads: command types, event types, the reason and outcome identifiers those events reference, and the `...Property` keys used... |
| [`BattleSnapshot`](commands-events-and-snapshots.md#battlesnapshot) | Commands, events and snapshots | Immutable snapshot of an entire battle at one tick: teams, combatants, resources, cooldowns, statuses, in-flight actions, the pending work queue, and the outcome so far. |
| [`PropertySet`](commands-events-and-snapshots.md#propertyset) | Commands, events and snapshots | The immutable, sorted, bounded property bag every mechanics extension is configured with: a formula, effect resolver, target resolver, AI policy, or reaction rule reads its authore... |
| [`BattleSchedulerRegistry`](scheduling-and-tempo.md#battleschedulerregistry) | Scheduling and tempo | The immutable set of turn-order schedulers a battle may use, keyed by scheduler ID and contract version, each stored with its canonical state codec and its optional scheduler-adjus... |
| [`BattleMechanicsRegistry`](effects-and-mechanics.md#battlemechanicsregistry) | Effects and mechanics | The immutable table that binds every formula, effect resolver, target resolver, AI policy, and reaction rule to an ID and a contract version. |
| [`IFormula`](effects-and-mechanics.md#iformula) | Effects and mechanics | Turns battle inputs into a damage or healing number. |
| [`BattleContentCatalog`](authoring-definitions.md#battlecontentcatalog) | Authoring definitions | The sole root of a closed authoring graph. |
| [`BattleRulesDefinition`](authoring-definitions.md#battlerulesdefinition) | Authoring definitions | The one set of rules every battle compiled from a catalog runs under: which stat assets carry the meanings the engine needs, which registered formulas it calls for damage, healing,... |
| [`BattleTemplate`](authoring-definitions.md#battletemplate) | Authoring definitions | One starting point for a battle: the turn model it runs under and the stage shape it is fought on, named and described together. |
| [`BattleTemplateDefaults`](authoring-definitions.md#battletemplatedefaults) | Authoring definitions | The shipped battle templates, defined in code rather than as serialized assets, for the same reason the shipped skins are: no asset is redistributed, so the provenance audit stays ... |
| [`CombatantDefinition`](authoring-definitions.md#combatantdefinition) | Authoring definitions | One reusable template for a fighter: the stats and resources it carries in, the skills it may use, the AI policy that drives it, and what it shrugs off. |
| [`CompiledBattleContent`](authoring-definitions.md#compiledbattlecontent) | Authoring definitions | The validated, read-only content a battle runs on: rules, stats, resources, combatants, skills, statuses, reactions, AI policies, schedulers, and the mechanics registry those defin... |
| [`EffectDefinition`](authoring-definitions.md#effectdefinition) | Authoring definitions | One reusable thing that happens to a target: the registered effect resolver that plans the work, the authored arguments handed to it, and the tags the effect publishes while it res... |
| [`EncounterDefinition`](authoring-definitions.md#encounterdefinition) | Authoring definitions | One playable fight: the two sides that meet, the formation each stands in, and the scheduler that decides who acts when. |
| [`ResourceDefinition`](authoring-definitions.md#resourcedefinition) | Authoring definitions | One spendable pool a combatant carries - mana, rage, ammunition, whatever the game calls it - defined only by the range it may hold. |
| [`SchedulerDefinition`](authoring-definitions.md#schedulerdefinition) | Authoring definitions | The turn order one encounter runs under: which scheduling model hands out opportunities to act, and the timing values that model reads. |
| [`SkillDefinition`](authoring-definitions.md#skilldefinition) | Authoring definitions | One action a combatant can take: how long it takes to cast and recover, what it costs, who it is allowed to hit, and the ordered effects it runs on each target it hits. |
| [`StatDefinition`](authoring-definitions.md#statdefinition) | Authoring definitions | One named number a combatant can carry, described only by the range it may hold. |
| [`StatusDefinition`](authoring-definitions.md#statusdefinition) | Authoring definitions | One condition that rides on a combatant for a while: how it stacks, how long it lasts, what it modifies while resident, and what it does on its own clock. |
| [`TargetDefinition`](authoring-definitions.md#targetdefinition) | Authoring definitions | One reusable answer to "who may this skill hit": the registered target resolver that picks and validates targets, plus the authored configuration handed to it. |
| [`TeamDefinition`](authoring-definitions.md#teamdefinition) | Authoring definitions | One reusable roster: the members that fight as a single side, each entry a combatant definition plus the state it starts the battle in. |
| [`AuthoringCompileRequest`](compiling-and-validating-content.md#authoringcompilerequest) | Compiling and validating content | Everything `BattleContentCompiler` needs for one compile: the catalog root to read, the scheduler and mechanics registries that authored references are resolved against, and the co... |
| [`AuthoringCompileResult`](compiling-and-validating-content.md#authoringcompileresult) | Compiling and validating content | The outcome of one compile: either a published `CatalogSnapshot` or the diagnostics that stopped it, never both and never neither. |
| [`BattleContentCompiler`](compiling-and-validating-content.md#battlecontentcompiler) | Compiling and validating content | The B4 mapping path converts captured authoring snapshots into the established B3 compiled-content model. |
| [`CompiledAuthoringCatalog`](compiling-and-validating-content.md#compiledauthoringcatalog) | Compiling and validating content | The published output of a successful compile: the compiled battle content, the registries it was resolved against, the encounters that can be started, and the hashes identifying al... |
| [`FormationPresetDefinition`](formations.md#formationpresetdefinition) | Formations | Mutable Unity authoring data. |
| [`BattleSkinPreset`](skinning-and-appearance.md#battleskinpreset) | Skinning and appearance | Every value the battle interface draws itself with, in one asset. |
| [`BattleNumberFormat`](interface-and-widgets.md#battlenumberformat) | Interface and widgets | Turns the simulation's fixed-point types into player-facing text. |
| [`BattleUiRoot`](interface-and-widgets.md#battleuiroot) | Interface and widgets | The battle interface. |
| [`DisplayStringTable`](interface-and-widgets.md#displaystringtable) | Interface and widgets | A non-authoritative map from stable id to display text. |
| [`BattlePresenter`](stage-and-tokens.md#battlepresenter) | Stage and tokens | The pure presentation consumer. |
| [`PresenterBinding`](stage-and-tokens.md#presenterbinding) | Stage and tokens | The explicit dependency bundle a driver hands to a `BattlePresenter`. |
| [`Chance64`](numerics-and-determinism.md#chance64) | Numerics and determinism | A deterministic probability value where 1,000,000 raw units equal 100%. |
| [`Fixed64`](numerics-and-determinism.md#fixed64) | Numerics and determinism | A signed fixed-point number carrying four decimal places, stored as a 64-bit integer in which 10,000 raw units make 1.0. |
| [`StableId`](numerics-and-determinism.md#stableid) | Numerics and determinism | The identifier every piece of content, state, and event in the simulation is named by: 1 to 128 characters drawn from a-z, 0-9, and the three punctuation characters '.', '_' and '-... |

## Every type

!!! tip "Filter as you type"
    Start typing in the box below to narrow the table. Use the search icon in the header to search the whole site instead.

<input type="text" id="api-filter" class="api-filter" placeholder="Filter types, groups, or descriptions..." autocomplete="off" aria-label="Filter API types">
<p id="api-filter-count" class="api-filter-count"></p>

<div class="api-table" markdown>

| Type | Kind | Area | What it is for |
| --- | --- | --- | --- |
| [`AdvanceTicksOutcome`](running-a-battle.md#advanceticksoutcome) | enum | Running a battle | Why one `BattleEngine.AdvanceTicks(int)` call stopped. |
| [`AdvanceTicksResult`](running-a-battle.md#advanceticksresult) | class | Running a battle | Immutable result of one `BattleEngine.AdvanceTicks(int)` call: the outcome that stopped it, the absolute tick it was aiming for, every event emitted on the way in strict tick and e... |
| [`BattleEngine`](running-a-battle.md#battleengine) | class | Running a battle | Owns immutable battle state and advances it through deterministic command, scheduler, action, event, and mechanics reduction boundaries. |
| [`BattleResultState`](running-a-battle.md#battleresultstate) | class | Running a battle | The battle's outcome as of one snapshot: either nonterminal (`None`) or a terminal verdict naming the result and, for team outcomes, the surviving and eliminated teams. |
| [`BattleStartRequest`](running-a-battle.md#battlestartrequest) | class | Running a battle | The immutable opening state of one battle: the scheduler that will run it, the two opposing teams, and the health, resources, and statuses every combatant starts with. |
| [`CommandDisposition`](running-a-battle.md#commanddisposition) | enum | Running a battle | How `BattleEngine.Submit(BattleCommand)` treated one command. |
| [`CommandResult`](running-a-battle.md#commandresult) | class | Running a battle | Immutable result of one `BattleEngine.Submit(BattleCommand)` call: how the command was treated, the single command event validation produced, and the resulting snapshot. |
| [`SimulationLimits`](running-a-battle.md#simulationlimits) | class | Running a battle | Every hard ceiling the simulation enforces, as compile-time constants. |
| [`StepActionOutcome`](running-a-battle.md#stepactionoutcome) | enum | Running a battle | Why one `BattleEngine.StepAction` call stopped. |
| [`StepActionResult`](running-a-battle.md#stepactionresult) | class | Running a battle | Immutable result of one `BattleEngine.StepAction` call: every event emitted while driving execution to the next action boundary, in emission order, plus the snapshot at that bounda... |
| [`StepEventOutcome`](running-a-battle.md#stepeventoutcome) | enum | Running a battle | Why one `BattleEngine.StepEvent` call stopped. |
| [`StepEventResult`](running-a-battle.md#stepeventresult) | class | Running a battle | Immutable result of one `BattleEngine.StepEvent` reduction: why the call stopped, the single event it emitted, and the authoritative snapshot that follows it. |
| [`ActionCostState`](commands-events-and-snapshots.md#actioncoststate) | class | Commands, events and snapshots | One line of an action's resource ledger: how much of one resource was paid, or refunded. |
| [`ActiveActionState`](commands-events-and-snapshots.md#activeactionstate) | class | Commands, events and snapshots | One action that has been accepted and has not finished resolving: its actor, skill, locked targets, cost ledger, and cast window. |
| [`ActiveCastState`](commands-events-and-snapshots.md#activecaststate) | class | Commands, events and snapshots | The cast window of an in-flight action. |
| [`BattleCommand`](commands-events-and-snapshots.md#battlecommand) | class | Commands, events and snapshots | One immutable decision handed to a battle: which combatant acts, on which tick, under which command type, and against what. |
| [`BattleEvent`](commands-events-and-snapshots.md#battleevent) | class | Commands, events and snapshots | One immutable gameplay event emitted by the battle engine: what happened, on which tick, in what order, and under which root action. |
| [`BattleIds`](commands-events-and-snapshots.md#battleids) | class | Commands, events and snapshots | The stable identifiers the battle simulation emits and reads: command types, event types, the reason and outcome identifiers those events reference, and the `...Property` keys used... |
| [`BattleSnapshot`](commands-events-and-snapshots.md#battlesnapshot) | class | Commands, events and snapshots | Immutable snapshot of an entire battle at one tick: teams, combatants, resources, cooldowns, statuses, in-flight actions, the pending work queue, and the outcome so far. |
| [`CombatantState`](commands-events-and-snapshots.md#combatantstate) | class | Commands, events and snapshots | Immutable per-combatant state held by a `BattleSnapshot`: identity, team, health bounds, target eligibility, and formation placement. |
| [`CooldownState`](commands-events-and-snapshots.md#cooldownstate) | class | Commands, events and snapshots | One skill still on cooldown for one combatant. |
| [`DecisionControlKind`](commands-events-and-snapshots.md#decisioncontrolkind) | enum | Commands, events and snapshots | Who fills a scheduled decision. |
| [`DecisionEntry`](commands-events-and-snapshots.md#decisionentry) | class | Commands, events and snapshots | One queued decision opportunity: an actor that became ready at a known tick and is waiting for its command. |
| [`PropertyEntry`](commands-events-and-snapshots.md#propertyentry) | struct | Commands, events and snapshots | One key and one tagged value, the element type of a PropertySet. |
| [`PropertySet`](commands-events-and-snapshots.md#propertyset) | class | Commands, events and snapshots | The immutable, sorted, bounded property bag every mechanics extension is configured with: a formula, effect resolver, target resolver, AI policy, or reaction rule reads its authore... |
| [`ResourceState`](commands-events-and-snapshots.md#resourcestate) | class | Commands, events and snapshots | One combatant's pool for one resource, such as mana or stamina. |
| [`StartTeam`](commands-events-and-snapshots.md#startteam) | class | Commands, events and snapshots | One side as a battle begins: its id and the combatants it fields. |
| [`TaggedValue`](commands-events-and-snapshots.md#taggedvalue) | class | Commands, events and snapshots | One immutable value carrying exactly one of the tagged payloads; it is the value half of a PropertySet and so the unit every mechanics extension is configured with. |
| [`TaggedValueTag`](commands-events-and-snapshots.md#taggedvaluetag) | enum | Commands, events and snapshots | Which payload a TaggedValue carries, and therefore the one accessor on it that may be read. |
| [`TeamState`](commands-events-and-snapshots.md#teamstate) | class | Commands, events and snapshots | Immutable state of one team in a `BattleSnapshot`. |
| [`ActionCostPaymentPolicy`](scheduling-and-tempo.md#actioncostpaymentpolicy) | enum | Scheduling and tempo | When an action's resource costs are debited. |
| [`ActionOrderScheduler`](scheduling-and-tempo.md#actionorderscheduler) | class | Scheduling and tempo | The built-in round-based scheduler: every eligible combatant is offered one opportunity per round, in ready-tick order, and the round closes once all of them have resolved. |
| [`ActionOrderSchedulerStateCodec`](scheduling-and-tempo.md#actionorderschedulerstatecodec) | class | Scheduling and tempo | The canonical state codec for the built-in Action Order scheduler, covering the decision queue, each actor's next ready tick, and the round bookkeeping. |
| [`ActionOrderState`](scheduling-and-tempo.md#actionorderstate) | class | Scheduling and tempo | The Action Order payload of a `SchedulerState`: per-actor ready ticks plus the round they are being spent in. |
| [`AtbScheduler`](scheduling-and-tempo.md#atbscheduler) | class | Scheduling and tempo | The built-in gauge-based scheduler: each combatant accrues its raw effective speed in gauge units per tick, and becomes ready when the gauge reaches the definition's threshold. |
| [`AtbSchedulerStateCodec`](scheduling-and-tempo.md#atbschedulerstatecodec) | class | Scheduling and tempo | The canonical state codec for the built-in ATB scheduler, covering the decision queue, the gauge threshold and input-pause policy, and each actor's gauge units and recovery lock. |
| [`AtbState`](scheduling-and-tempo.md#atbstate) | class | Scheduling and tempo | The ATB payload of a `SchedulerState`: the gauge threshold, the input-pause policy in force, and every actor's gauge. |
| [`BattleForecast`](scheduling-and-tempo.md#battleforecast) | class | Scheduling and tempo | Read-only lookahead over a live battle. |
| [`BattleSchedulerRegistry`](scheduling-and-tempo.md#battleschedulerregistry) | class | Scheduling and tempo | The immutable set of turn-order schedulers a battle may use, keyed by scheduler ID and contract version, each stored with its canonical state codec and its optional scheduler-adjus... |
| [`CompiledActionCost`](scheduling-and-tempo.md#compiledactioncost) | class | Scheduling and tempo | One resource cost of an action: which resource is spent, and how much. |
| [`CompiledSkillTiming`](scheduling-and-tempo.md#compiledskilltiming) | class | Scheduling and tempo | The compiled timing, cooldown, cost, and target-count contract for one skill. |
| [`CooldownClockKind`](scheduling-and-tempo.md#cooldownclockkind) | enum | Scheduling and tempo | The clock a cooldown counts down on. |
| [`CooldownStartPolicy`](scheduling-and-tempo.md#cooldownstartpolicy) | enum | Scheduling and tempo | When a skill's cooldown clock starts. |
| [`GaugeEntry`](scheduling-and-tempo.md#gaugeentry) | class | Scheduling and tempo | One ATB actor's gauge: how far it has filled toward the scheduler's threshold, plus the tick until which filling stays suppressed after the actor acted. |
| [`IBattleScheduler`](scheduling-and-tempo.md#ibattlescheduler) | interface | Scheduling and tempo | The pure turn-order contract. |
| [`ISchedulerAdjustmentAdapter`](scheduling-and-tempo.md#ischeduleradjustmentadapter) | interface | Scheduling and tempo | Lets an effect retime one actor inside a scheduler's state - hasten it, delay it, or push its ATB gauge - without the effect knowing how that scheduler measures time. |
| [`ISchedulerAdjustmentAdapterProvider`](scheduling-and-tempo.md#ischeduleradjustmentadapterprovider) | interface | Scheduling and tempo | Implemented by a scheduler that carries its own adjustment adapter, so `BattleSchedulerRegistry.Register(IBattleScheduler)` picks it up without the caller naming it separately. |
| [`ISchedulerStateCodec`](scheduling-and-tempo.md#ischedulerstatecodec) | interface | Scheduling and tempo | The canonical byte form of one scheduler's state. |
| [`ISchedulerStateCodecProvider`](scheduling-and-tempo.md#ischedulerstatecodecprovider) | interface | Scheduling and tempo | Implemented by a scheduler that carries its own canonical state codec, so it can be handed to `BattleSchedulerRegistry.Register(IBattleScheduler)` without the caller naming the cod... |
| [`InputPausePolicy`](scheduling-and-tempo.md#inputpausepolicy) | enum | Scheduling and tempo | What the ATB scheduler does with time while a human decision is pending. |
| [`InterruptRefundPolicy`](scheduling-and-tempo.md#interruptrefundpolicy) | enum | Scheduling and tempo | What happens to the costs already paid for an action whose cast is interrupted. |
| [`ReadyTickEntry`](scheduling-and-tempo.md#readytickentry) | class | Scheduling and tempo | The earliest tick at which one Action Order actor may next be offered an opportunity. |
| [`RoundState`](scheduling-and-tempo.md#roundstate) | class | Scheduling and tempo | One Action Order round: the participants snapshotted when the round began and the subset that has already resolved. |
| [`SchedulerAdjustmentContext`](scheduling-and-tempo.md#scheduleradjustmentcontext) | class | Scheduling and tempo | Immutable input to `ISchedulerAdjustmentAdapter.Apply`: which actor is being retimed, whether its ready tick or its ATB gauge moves, and by how much. |
| [`SchedulerAdjustmentResult`](scheduling-and-tempo.md#scheduleradjustmentresult) | class | Scheduling and tempo | Outcome of `ISchedulerAdjustmentAdapter.Apply`: the scheduler state after the adjustment, how much of the requested delta survived clamping, and any readiness the adjustment itself... |
| [`SchedulerAdvanceContext`](scheduling-and-tempo.md#scheduleradvancecontext) | class | Scheduling and tempo | Immutable input to `IBattleScheduler.Advance`: the current tick, one timing view per combatant, the next opportunity sequence the scheduler may allocate, the engine's due timers, a... |
| [`SchedulerAdvanceResult`](scheduling-and-tempo.md#scheduleradvanceresult) | class | Scheduling and tempo | Outcome of `IBattleScheduler.Advance`: the next scheduler state, the ordered work for the engine to translate, and why the transition stopped. |
| [`SchedulerAdvanceStopReason`](scheduling-and-tempo.md#scheduleradvancestopreason) | enum | Scheduling and tempo | Why `IBattleScheduler.Advance` stopped. |
| [`SchedulerCombatantTimingView`](scheduling-and-tempo.md#schedulercombatanttimingview) | class | Scheduling and tempo | Immutable per-actor timing input the engine builds for one scheduler transition. |
| [`SchedulerCreateContext`](scheduling-and-tempo.md#schedulercreatecontext) | class | Scheduling and tempo | Immutable input to `IBattleScheduler.Create`: the compiled definition to honour, the tick the state is created at, and one timing view per combatant. |
| [`SchedulerCreateResult`](scheduling-and-tempo.md#schedulercreateresult) | class | Scheduling and tempo | Outcome of `IBattleScheduler.Create`. |
| [`SchedulerDiagnosticIds`](scheduling-and-tempo.md#schedulerdiagnosticids) | class | Scheduling and tempo | The stable diagnostic IDs the registry and the built-in schedulers report. |
| [`SchedulerDueTimer`](scheduling-and-tempo.md#schedulerduetimer) | class | Scheduling and tempo | One engine-owned boundary the scheduler must stop at. |
| [`SchedulerDueTimerKind`](scheduling-and-tempo.md#schedulerduetimerkind) | enum | Scheduling and tempo | The engine-owned timer categories a scheduler must not advance past. |
| [`SchedulerOpportunityContext`](scheduling-and-tempo.md#scheduleropportunitycontext) | class | Scheduling and tempo | Immutable input to `IBattleScheduler.OnOpportunityAccepted`, naming the queued decision the engine is about to consume. |
| [`SchedulerOpportunityOutcome`](scheduling-and-tempo.md#scheduleropportunityoutcome) | enum | Scheduling and tempo | How an opportunity ended, as reported to `IBattleScheduler.OnOpportunityFinished`. |
| [`SchedulerOpportunityResult`](scheduling-and-tempo.md#scheduleropportunityresult) | class | Scheduling and tempo | Immutable report that one opportunity has finished, and the input to `IBattleScheduler.OnOpportunityFinished`. |
| [`SchedulerState`](scheduling-and-tempo.md#schedulerstate) | class | Scheduling and tempo | The authoritative scheduler half of a battle snapshot: the ordered decision queue plus exactly one family payload chosen by `StateTag`. |
| [`SchedulerStateDecodeResult`](scheduling-and-tempo.md#schedulerstatedecoderesult) | class | Scheduling and tempo | The outcome of rebuilding a `SchedulerState` from payload bytes: either the state, or the diagnostic saying it could not be read. |
| [`SchedulerStateTag`](scheduling-and-tempo.md#schedulerstatetag) | enum | Scheduling and tempo | Discriminates which payload a `SchedulerState` carries. |
| [`SchedulerTransitionResult`](scheduling-and-tempo.md#schedulertransitionresult) | class | Scheduling and tempo | Outcome of an opportunity transition, either `IBattleScheduler.OnOpportunityAccepted` or `IBattleScheduler.OnOpportunityFinished`. |
| [`SchedulerWork`](scheduling-and-tempo.md#schedulerwork) | class | Scheduling and tempo | One ordered unit of scheduler output: a closed union whose payload the engine copies into execution frames. |
| [`SchedulerWorkTag`](scheduling-and-tempo.md#schedulerworktag) | enum | Scheduling and tempo | The closed set of work a scheduler can return, and the tag that says which payload of `SchedulerWork` is populated. |
| [`TimingResolutionKind`](scheduling-and-tempo.md#timingresolutionkind) | enum | Scheduling and tempo | Timing-layer work a skill performs as it resolves, on top of its own effects. |
| [`AiValidationContext`](effects-and-mechanics.md#aivalidationcontext) | class | Effects and mechanics | Read-only catalog passed to IAiPolicy.Validate while compiled content is being built. |
| [`BattleFormulaService`](effects-and-mechanics.md#battleformulaservice) | class | Effects and mechanics | Pure formula input and evaluation boundary shared by runtime, forecast, replay, Workbench, tooltips, and range previews. |
| [`BattleMechanicsRegistry`](effects-and-mechanics.md#battlemechanicsregistry) | class | Effects and mechanics | The immutable table that binds every formula, effect resolver, target resolver, AI policy, and reaction rule to an ID and a contract version. |
| [`BattleStateView`](effects-and-mechanics.md#battlestateview) | class | Effects and mechanics | Immutable, RNG-free projection supplied to non-formula mechanics extensions. |
| [`EffectPlan`](effects-and-mechanics.md#effectplan) | class | Effects and mechanics | What one effect entry expands into: the primitives to execute, in order, plus any diagnostics that make the expansion unusable. |
| [`EffectPlanningContext`](effects-and-mechanics.md#effectplanningcontext) | class | Effects and mechanics | Frozen inputs for one call to IEffectResolver.Plan: the compiled catalog, a read-only view of the battle state, and the source, target, and effect entry being planned. |
| [`EffectPrimitive`](effects-and-mechanics.md#effectprimitive) | class | Effects and mechanics | One immutable unit of work an effect resolver asks the engine to perform. |
| [`EffectPrimitiveTag`](effects-and-mechanics.md#effectprimitivetag) | enum | Effects and mechanics | The operation one planned primitive performs. |
| [`EffectValidationContext`](effects-and-mechanics.md#effectvalidationcontext) | class | Effects and mechanics | Read-only catalog passed to IEffectResolver.Validate while compiled content is being built. |
| [`FormulaAttribution`](effects-and-mechanics.md#formulaattribution) | class | Effects and mechanics | The complete, immutable account of one formula evaluation: the inputs it read, every step it applied, every random draw it took, and the values it ended on. |
| [`FormulaAttributionTrace`](effects-and-mechanics.md#formulaattributiontrace) | class | Effects and mechanics | Consumer-owned evidence linking full formula attribution bytes to the gameplay event that references their hash. |
| [`FormulaAttributionTraceBatch`](effects-and-mechanics.md#formulaattributiontracebatch) | class | Effects and mechanics | Bounded immutable formula evidence returned to one consumer call. |
| [`FormulaContext`](effects-and-mechanics.md#formulacontext) | class | Effects and mechanics | Every input one formula evaluation is allowed to read, frozen before the first draw. |
| [`FormulaContribution`](effects-and-mechanics.md#formulacontribution) | struct | Effects and mechanics | One recorded step of a formula evaluation: the value that entered the step and the value that left it. |
| [`FormulaContributionKind`](effects-and-mechanics.md#formulacontributionkind) | enum | Effects and mechanics | Classifies individual formula contribution kind stages recorded by formula attribution. |
| [`FormulaEvaluationRequest`](effects-and-mechanics.md#formulaevaluationrequest) | class | Effects and mechanics | Immutable coordinates for one formula primitive. |
| [`FormulaModifierInput`](effects-and-mechanics.md#formulamodifierinput) | struct | Effects and mechanics | One status-supplied modifier already resolved into a formula input. |
| [`FormulaPreview`](effects-and-mechanics.md#formulapreview) | class | Effects and mechanics | What a formula would produce, reported for tooltips and other passive display: the value range of a use that lands, plus the chances the formula reports. |
| [`FormulaPreviewContext`](effects-and-mechanics.md#formulapreviewcontext) | class | Effects and mechanics | Marks an evaluation as a preview: the same inputs as the live call, but no RNG and no state change. |
| [`FormulaRandomBoundKind`](effects-and-mechanics.md#formularandomboundkind) | enum | Effects and mechanics | How a declared random input states the exclusive upper bound its draw will use. |
| [`FormulaRandomInputDescriptor`](effects-and-mechanics.md#formularandominputdescriptor) | struct | Effects and mechanics | One RNG draw a formula promises to take, in the order it will be taken. |
| [`FormulaRandomSample`](effects-and-mechanics.md#formularandomsample) | struct | Effects and mechanics | One random draw a formula took, recorded as the bound it asked for and the raw value it received. |
| [`FormulaResult`](effects-and-mechanics.md#formularesult) | class | Effects and mechanics | What one formula evaluation produced: whether it landed, whether it crit, the final clamped magnitude, and the attribution the engine hashes into the resulting event. |
| [`FormulaValidationContext`](effects-and-mechanics.md#formulavalidationcontext) | class | Effects and mechanics | Read-only catalog passed to IFormula.Validate while compiled content is being built. |
| [`IAiPolicy`](effects-and-mechanics.md#iaipolicy) | interface | Effects and mechanics | Proposes, in preference order, the skill uses an AI-controlled combatant would like to make. |
| [`IEffectResolver`](effects-and-mechanics.md#ieffectresolver) | interface | Effects and mechanics | Expands one authored effect entry into the ordered primitives the engine will execute: damage, healing, resource change, shield, status apply or remove, dispel, scheduler adjustmen... |
| [`IFormula`](effects-and-mechanics.md#iformula) | interface | Effects and mechanics | Turns battle inputs into a damage or healing number. |
| [`IMechanicsImplementation`](effects-and-mechanics.md#imechanicsimplementation) | interface | Effects and mechanics | Identity carried by every mechanics extension registered in a BattleMechanicsRegistry. |
| [`IMechanicsRandomSource`](effects-and-mechanics.md#imechanicsrandomsource) | interface | Effects and mechanics | The engine-owned draw cursor handed to a formula for one evaluation. |
| [`IReactionRule`](effects-and-mechanics.md#ireactionrule) | interface | Effects and mechanics | Decides whether a queued reaction actually fires when a tagged effect resolves, and which pair of combatants it fires between. |
| [`ITargetResolver`](effects-and-mechanics.md#itargetresolver) | interface | Effects and mechanics | Decides which combatants a skill may hit and whether the targets a player or an AI asked for are legal. |
| [`MechanicsCategoryTag`](effects-and-mechanics.md#mechanicscategorytag) | enum | Effects and mechanics | Which of the five mechanics extension interfaces an implementation was registered under. |
| [`MechanicsDiagnosticIds`](effects-and-mechanics.md#mechanicsdiagnosticids) | class | Effects and mechanics | The IDs the mechanics layer reports its diagnostics under: registry binding failures, rejected authored properties, missing or over-large content, formula contract violations, unus... |
| [`MechanicsIds`](effects-and-mechanics.md#mechanicsids) | class | Effects and mechanics | The stable IDs the shipped formulas, effect resolvers, target resolvers, AI policies, and reaction rules register themselves under, together with the property keys those implementa... |
| [`MechanicsRegistryBinding`](effects-and-mechanics.md#mechanicsregistrybinding) | struct | Effects and mechanics | The full key one registry entry is filed under: category, implementation ID, and contract version. |
| [`MechanicsResolveResult`](effects-and-mechanics.md#mechanicsresolveresult) | class | Effects and mechanics | The outcome of one registry lookup: either the implementation or the diagnostic explaining why it could not be resolved, never both. |
| [`ReactionValidationContext`](effects-and-mechanics.md#reactionvalidationcontext) | class | Effects and mechanics | Read-only catalog passed to IReactionRule.Validate while compiled content is being built. |
| [`SchedulerAdjustmentKind`](effects-and-mechanics.md#scheduleradjustmentkind) | enum | Effects and mechanics | The timing value an AdjustScheduler primitive moves. |
| [`StatusApplicationPreview`](effects-and-mechanics.md#statusapplicationpreview) | class | Effects and mechanics | RNG-free status application calculation used by runtime and tooltips. |
| [`TargetValidationContext`](effects-and-mechanics.md#targetvalidationcontext) | class | Effects and mechanics | Read-only catalog passed to ITargetResolver.Validate while compiled content is being built. |
| [`ValidationReport`](effects-and-mechanics.md#validationreport) | class | Effects and mechanics | What a validator found: the diagnostics that make the thing unusable, and the ones that are merely worth saying. |
| [`CombatantStatState`](statuses-targeting-and-reactions.md#combatantstatstate) | class | Statuses, targeting and reactions | One combatant's base value for one stat, as carried by a snapshot. |
| [`ReactionContext`](statuses-targeting-and-reactions.md#reactioncontext) | class | Statuses, targeting and reactions | Everything a reaction rule may look at while deciding one candidate: the triggering effect tag and phase, the two combatants involved, the compiled catalog, and a read-only view of... |
| [`ReactionEvaluation`](statuses-targeting-and-reactions.md#reactionevaluation) | class | Statuses, targeting and reactions | A reaction rule's verdict on one candidate: whether it fires, and the source and target it will use if it does. |
| [`ReactionSignature`](statuses-targeting-and-reactions.md#reactionsignature) | class | Statuses, targeting and reactions | The static contract an `IReactionRule` publishes: which effect tags may trigger it and which effect tags it can go on to emit. |
| [`ShieldState`](statuses-targeting-and-reactions.md#shieldstate) | class | Statuses, targeting and reactions | One shield absorbing damage for a combatant. |
| [`StatusInstanceState`](statuses-targeting-and-reactions.md#statusinstancestate) | class | Statuses, targeting and reactions | One live status application on one combatant: where it came from, how many stacks it carries, how much duration is left, and when it next ticks. |
| [`TargetContext`](statuses-targeting-and-reactions.md#targetcontext) | class | Statuses, targeting and reactions | Everything a target resolver is given about the situation it is choosing for: the compiled catalog, who is acting, which skill is being used, and a read-only projection of battle s... |
| [`TargetLifeState`](statuses-targeting-and-reactions.md#targetlifestate) | enum | Statuses, targeting and reactions | Which life state a combatant must be in to be an eligible target. |
| [`TargetRequestContract`](statuses-targeting-and-reactions.md#targetrequestcontract) | class | Statuses, targeting and reactions | The declared shape of one target resolver's requests: how many target IDs a command may carry, whether an empty request means the resolver selects, how many targets the engine draw... |
| [`TargetRequestResult`](statuses-targeting-and-reactions.md#targetrequestresult) | class | Statuses, targeting and reactions | A target resolver's verdict on one request: either the set of targets to lock, or the diagnostic explaining the refusal. |
| [`TargetTeamRelation`](statuses-targeting-and-reactions.md#targetteamrelation) | enum | Statuses, targeting and reactions | Which combatants a target request may reach, relative to the acting combatant's team. |
| [`AiCandidateDescription`](ai-policies.md#aicandidatedescription) | class | AI policies | One action a policy puts forward for consideration: the authored rule it comes from, the skill to use, and the targets to request. |
| [`AiCandidatePlan`](ai-policies.md#aicandidateplan) | class | AI policies | The candidates a policy returns for one decision opportunity, in preference order. |
| [`AiCandidateTrace`](ai-policies.md#aicandidatetrace) | class | AI policies | Per-candidate record of why one proposed action was or was not eligible, including the conditions that were evaluated for it and the diagnostic that rejected it. |
| [`AiConditionTrace`](ai-policies.md#aiconditiontrace) | struct | AI policies | Record of one authored condition being evaluated for a rule during an AI decision. |
| [`AiContext`](ai-policies.md#aicontext) | class | AI policies | Read-only input handed to an `IAiPolicy` when the engine asks it to propose candidates for a single decision opportunity. |
| [`AiDecisionTrace`](ai-policies.md#aidecisiontrace) | class | AI policies | Complete audit record of one automatic decision: every candidate considered and why it was kept or dropped, every random draw consumed to choose among them and to resolve targets, ... |
| [`AiConditionDefinition`](authoring-definitions.md#aiconditiondefinition) | class | Authoring definitions | One gate on an `AiRuleDefinition`. |
| [`AiConditionKind`](authoring-definitions.md#aiconditionkind) | enum | Authoring definitions | The tests an AI rule may gate itself on. |
| [`AiPolicyDefinition`](authoring-definitions.md#aipolicydefinition) | class | Authoring definitions | One reusable answer to "what does this combatant do when it gets an opportunity": the registered AI policy that decides, the authored configuration handed to it, and the candidate ... |
| [`AiRuleDefinition`](authoring-definitions.md#airuledefinition) | class | Authoring definitions | One candidate action inside an `AiPolicyDefinition`: the skill to use, the conditions that must all hold before it may be chosen, and the ordering data the policy selects with. |
| [`AuthoringValueTag`](authoring-definitions.md#authoringvaluetag) | enum | Authoring definitions | Which of a `PropertyEntryDefinition`'s value slots is the live one. |
| [`BattleContentCatalog`](authoring-definitions.md#battlecontentcatalog) | class | Authoring definitions | The sole root of a closed authoring graph. |
| [`BattleResultPolicyKind`](authoring-definitions.md#battleresultpolicykind) | enum | Authoring definitions | How a battle's terminal result is decided. |
| [`BattleRulesDefinition`](authoring-definitions.md#battlerulesdefinition) | class | Authoring definitions | The one set of rules every battle compiled from a catalog runs under: which stat assets carry the meanings the engine needs, which registered formulas it calls for damage, healing,... |
| [`BattleTemplate`](authoring-definitions.md#battletemplate) | class | Authoring definitions | One starting point for a battle: the turn model it runs under and the stage shape it is fought on, named and described together. |
| [`BattleTemplateDefaults`](authoring-definitions.md#battletemplatedefaults) | class | Authoring definitions | The shipped battle templates, defined in code rather than as serialized assets, for the same reason the shipped skins are: no asset is redistributed, so the provenance audit stays ... |
| [`CombatantDefinition`](authoring-definitions.md#combatantdefinition) | class | Authoring definitions | One reusable template for a fighter: the stats and resources it carries in, the skills it may use, the AI policy that drives it, and what it shrugs off. |
| [`CombatantResourceEntryDefinition`](authoring-definitions.md#combatantresourceentrydefinition) | class | Authoring definitions | One entry in a `CombatantDefinition`'s resource default list: the resource, and how much of it the combatant starts with unless an encounter's team member entry overrides that reso... |
| [`CombatantStatEntryDefinition`](authoring-definitions.md#combatantstatentrydefinition) | class | Authoring definitions | One entry in a `CombatantDefinition`'s base stat list: the stat, and the value that combatant carries into battle. |
| [`CompiledAiCondition`](authoring-definitions.md#compiledaicondition) | class | Authoring definitions | One gate on an AI rule. |
| [`CompiledAiPolicyDefinition`](authoring-definitions.md#compiledaipolicydefinition) | class | Authoring definitions | One AI policy after compilation: the policy implementation to run and the rules it chooses between. |
| [`CompiledAiRule`](authoring-definitions.md#compiledairule) | class | Authoring definitions | One candidate action inside an AI policy: a skill to use, the conditions that must all hold first, and the ordering data the policy selects with. |
| [`CompiledBattleContent`](authoring-definitions.md#compiledbattlecontent) | class | Authoring definitions | The validated, read-only content a battle runs on: rules, stats, resources, combatants, skills, statuses, reactions, AI policies, schedulers, and the mechanics registry those defin... |
| [`CompiledCombatantDefinition`](authoring-definitions.md#compiledcombatantdefinition) | class | Authoring definitions | The compiled, immutable archetype a combatant is spawned from: its base stats, starting resources, granted skills, tags, status resistances, status immunities and intrinsic reactio... |
| [`CompiledEffectEntry`](authoring-definitions.md#compiledeffectentry) | class | Authoring definitions | One authored effect slot on a skill, status, or reaction: which registered effect resolver runs and with which authored arguments. |
| [`CompiledSkillDefinition`](authoring-definitions.md#compiledskilldefinition) | class | Authoring definitions | One usable skill after compilation: its timing, how it picks and keeps targets, and the ordered effect entries it runs. |
| [`CompiledStatusDefinition`](authoring-definitions.md#compiledstatusdefinition) | class | Authoring definitions | One status after compilation: how it stacks, how long it lasts, what it modifies while resident, and what it costs its owner. |
| [`EffectDefinition`](authoring-definitions.md#effectdefinition) | class | Authoring definitions | One reusable thing that happens to a target: the registered effect resolver that plans the work, the authored arguments handed to it, and the tags the effect publishes while it res... |
| [`EffectUseDefinition`](authoring-definitions.md#effectusedefinition) | class | Authoring definitions | One slot in an owner's effect list: the effect to run, plus an id that names the slot inside that owner. |
| [`EncounterDefinition`](authoring-definitions.md#encounterdefinition) | class | Authoring definitions | One playable fight: the two sides that meet, the formation each stands in, and the scheduler that decides who acts when. |
| [`EncounterTeamDefinition`](authoring-definitions.md#encounterteamdefinition) | class | Authoring definitions | One of the two sides of an `EncounterDefinition`: the roster that fights, the formation it fights in, and where each of its members stands. |
| [`FormationAssignmentDefinition`](authoring-definitions.md#formationassignmentdefinition) | class | Authoring definitions | Places one team member in one formation slot. |
| [`InitialStatusApplicationDefinition`](authoring-definitions.md#initialstatusapplicationdefinition) | class | Authoring definitions | One status already applied to a team member when the battle starts, before the first tick is simulated. |
| [`InvalidTargetPolicy`](authoring-definitions.md#invalidtargetpolicy) | enum | Authoring definitions | What the engine does when a locked target is no longer valid at resolution. |
| [`MechanicsImplementationReference`](authoring-definitions.md#mechanicsimplementationreference) | struct | Authoring definitions | An immutable pointer from compiled content to one registered mechanics implementation: its stable ID plus the contract version the content was authored against. |
| [`MechanicsImplementationReferenceDefinition`](authoring-definitions.md#mechanicsimplementationreferencedefinition) | class | Authoring definitions | The inspector form of a pointer to one registered mechanics implementation. |
| [`ModifierStage`](authoring-definitions.md#modifierstage) | enum | Authoring definitions | Which step of the deterministic stat and formula pipeline a status modifier joins. |
| [`PropertyEntryDefinition`](authoring-definitions.md#propertyentrydefinition) | class | Authoring definitions | One authored property: a key, a tag saying which value slot is live, and that value. |
| [`PropertySetDefinition`](authoring-definitions.md#propertysetdefinition) | class | Authoring definitions | The serialized bag of authored key/value properties on a definition: the arguments handed to whichever mechanics implementation that definition points at. |
| [`ReactionDefinition`](authoring-definitions.md#reactiondefinition) | class | Authoring definitions | One rule that lets a combatant act out of turn: the registered reaction rule that judges each candidate, when in a triggering effect's resolution it is offered, and the effects it ... |
| [`ReactionTriggerPhase`](authoring-definitions.md#reactiontriggerphase) | enum | Authoring definitions | Whether a reaction rule is offered before or after the primitive that triggers it. |
| [`ResistanceMatchKind`](authoring-definitions.md#resistancematchkind) | enum | Authoring definitions | Whether a combatant's resistance entry is keyed by a status definition ID or by a status tag. |
| [`ResourceDefinition`](authoring-definitions.md#resourcedefinition) | class | Authoring definitions | One spendable pool a combatant carries - mana, rage, ammunition, whatever the game calls it - defined only by the range it may hold. |
| [`SchedulerDefinition`](authoring-definitions.md#schedulerdefinition) | class | Authoring definitions | The turn order one encounter runs under: which scheduling model hands out opportunities to act, and the timing values that model reads. |
| [`SkillCostDefinition`](authoring-definitions.md#skillcostdefinition) | class | Authoring definitions | One resource a skill spends to be used. |
| [`SkillDefinition`](authoring-definitions.md#skilldefinition) | class | Authoring definitions | One action a combatant can take: how long it takes to cast and recover, what it costs, who it is allowed to hit, and the ordered effects it runs on each target it hits. |
| [`StableIdDefinition`](authoring-definitions.md#stableiddefinition) | class | Authoring definitions | Base class for authoring assets whose identity survives file, folder, label, and localization changes. |
| [`StartCombatantV3`](authoring-definitions.md#startcombatantv3) | class | Authoring definitions | The opening state of one combatant: the compiled definition it is built from, who decides for it, and the health, resources, statuses, and formation slot it starts with. |
| [`StartResourceV3`](authoring-definitions.md#startresourcev3) | struct | Authoring definitions | One resource pool a combatant holds at the first tick, as a definition id and an amount. |
| [`StartStatusApplicationV3`](authoring-definitions.md#startstatusapplicationv3) | class | Authoring definitions | One status a combatant already carries when the battle opens. |
| [`StartTeamV3`](authoring-definitions.md#startteamv3) | class | Authoring definitions | One side of a battle: a team id and the combatants fighting under it. |
| [`StartingHealthMode`](authoring-definitions.md#startinghealthmode) | enum | Authoring definitions | Chooses where a team member's starting current health comes from. |
| [`StatDefinition`](authoring-definitions.md#statdefinition) | class | Authoring definitions | One named number a combatant can carry, described only by the range it may hold. |
| [`StatusDefinition`](authoring-definitions.md#statusdefinition) | class | Authoring definitions | One condition that rides on a combatant for a while: how it stacks, how long it lasts, what it modifies while resident, and what it does on its own clock. |
| [`StatusDurationClock`](authoring-definitions.md#statusdurationclock) | enum | Authoring definitions | Which clock decrements a status instance's remaining duration: the owner's action start, the owner's action end, the owner's scheduler opportunity, or elapsed battle ticks. |
| [`StatusModifierDefinition`](authoring-definitions.md#statusmodifierdefinition) | class | Authoring definitions | One adjustment a `StatusDefinition` applies for as long as it is active. |
| [`StatusPeriodicPhase`](authoring-definitions.md#statusperiodicphase) | enum | Authoring definitions | When a status's periodic effects fire. |
| [`StatusPolarity`](authoring-definitions.md#statuspolarity) | enum | Authoring definitions | Whether a status reads as helpful, harmful, or neither. |
| [`StatusResistanceDefinition`](authoring-definitions.md#statusresistancedefinition) | class | Authoring definitions | One resistance entry on a `CombatantDefinition`, cutting the chance that a status lands on it. |
| [`StatusStackPolicy`](authoring-definitions.md#statusstackpolicy) | enum | Authoring definitions | How a fresh application of a status interacts with an instance the target already carries. |
| [`TargetDefinition`](authoring-definitions.md#targetdefinition) | class | Authoring definitions | One reusable answer to "who may this skill hit": the registered target resolver that picks and validates targets, plus the authored configuration handed to it. |
| [`TargetLockPolicy`](authoring-definitions.md#targetlockpolicy) | enum | Authoring definitions | When a skill captures the target IDs it will act on. |
| [`TeamDefinition`](authoring-definitions.md#teamdefinition) | class | Authoring definitions | One reusable roster: the members that fight as a single side, each entry a combatant definition plus the state it starts the battle in. |
| [`TeamMemberDefinition`](authoring-definitions.md#teammemberdefinition) | class | Authoring definitions | One roster entry of a `TeamDefinition`: which combatant definition is instantiated and the state it starts the battle in. |
| [`TeamMemberResourceOverrideDefinition`](authoring-definitions.md#teammemberresourceoverridedefinition) | class | Authoring definitions | Overrides the starting amount of one resource for a single team member. |
| [`AuthoringCompileOptions`](compiling-and-validating-content.md#authoringcompileoptions) | class | Compiling and validating content | The two knobs a compile takes: how it can be stopped, and whether warnings are reported alongside errors. |
| [`AuthoringCompileRequest`](compiling-and-validating-content.md#authoringcompilerequest) | class | Compiling and validating content | Everything `BattleContentCompiler` needs for one compile: the catalog root to read, the scheduler and mechanics registries that authored references are resolved against, and the co... |
| [`AuthoringCompileResult`](compiling-and-validating-content.md#authoringcompileresult) | class | Compiling and validating content | The outcome of one compile: either a published `CatalogSnapshot` or the diagnostics that stopped it, never both and never neither. |
| [`AuthoringDiagnostic`](compiling-and-validating-content.md#authoringdiagnostic) | class | Compiling and validating content | One problem found in authored content: which problem it is (`DiagnosticId`), how serious it is (`Severity`), and where in the authored data it sits (`Source`). |
| [`AuthoringDiagnosticSeverity`](compiling-and-validating-content.md#authoringdiagnosticseverity) | enum | Compiling and validating content | How serious an `AuthoringDiagnostic` is. |
| [`AuthoringLimits`](compiling-and-validating-content.md#authoringlimits) | class | Compiling and validating content | The structural ceilings authoring compilation enforces: how many definitions one catalog may reference, how many teams, encounters, and formation presets it may hold, the ranges no... |
| [`AuthoringValidationReport`](compiling-and-validating-content.md#authoringvalidationreport) | class | Compiling and validating content | The diagnostics half of a compile, returned by `BattleContentCompiler.Validate`. |
| [`BattleContentCompiler`](compiling-and-validating-content.md#battlecontentcompiler) | class | Compiling and validating content | The B4 mapping path converts captured authoring snapshots into the established B3 compiled-content model. |
| [`BattleRegistryProvider`](compiling-and-validating-content.md#battleregistryprovider) | class | Compiling and validating content | Project-owned extension point for custom schedulers and mechanics. |
| [`BattleRegistrySet`](compiling-and-validating-content.md#battleregistryset) | class | Compiling and validating content | One matched scheduler/mechanics registry pair. |
| [`CompiledAuthoringCatalog`](compiling-and-validating-content.md#compiledauthoringcatalog) | class | Compiling and validating content | The published output of a successful compile: the compiled battle content, the registries it was resolved against, the encounters that can be started, and the hashes identifying al... |
| [`CompiledEncounterSnapshot`](compiling-and-validating-content.md#compiledencountersnapshot) | class | Compiling and validating content | One authored encounter compiled into the exact inputs a battle starts from: the start request, the formation layout the stage is built from, and the digest identifying that start. |
| [`FrozenSortedIndex`](compiling-and-validating-content.md#frozensortedindex) | class | Compiling and validating content | A defensively copied, key-sorted immutable index. |
| [`AspectRatio`](formations.md#aspectratio) | struct | Formations | The design aspect a formation was authored against, as an exact integer fraction where `Numerator` is the width term and `Denominator` the height term. |
| [`CompiledEncounterFormationLayout`](formations.md#compiledencounterformationlayout) | class | Formations | The compiled formation for a whole encounter: exactly two teams, plus a flattened and indexed view of every combatant's seat. |
| [`CompiledEncounterFormationTeam`](formations.md#compiledencounterformationteam) | class | Formations | One team's half of a compiled encounter layout: the preset it stands in and which combatant holds which seat. |
| [`CompiledFormationAnchor`](formations.md#compiledformationanchor) | struct | Formations | One named attachment point on a compiled slot. |
| [`CompiledFormationPreset`](formations.md#compiledformationpreset) | class | Formations | A validated, immutable formation preset: the seats one team can occupy, plus the design aspect their coordinates were authored against. |
| [`CompiledFormationSlot`](formations.md#compiledformationslot) | class | Formations | One validated seat in a compiled formation preset: where a combatant stands, which way it faces, how it sorts against the other seats, and where its anchors are. |
| [`FormationArrangement`](formations.md#formationarrangement) | enum | Formations | The stage shapes a battle can be laid out in. |
| [`FormationArrangements`](formations.md#formationarrangements) | class | Formations | Builds formation presets for the shipped stage arrangements. |
| [`FormationFacing`](formations.md#formationfacing) | enum | Formations | Which way the occupant of a formation slot is presented as facing. |
| [`FormationOccupancy`](formations.md#formationoccupancy) | struct | Formations | The resolved binding of one combatant to one seat, with the team, preset, row and side that seat belongs to copied in so a consumer never has to walk back to the preset to draw or ... |
| [`FormationPoint`](formations.md#formationpoint) | struct | Formations | A resolution-independent position inside a formation preset. |
| [`FormationPresetDefinition`](formations.md#formationpresetdefinition) | class | Formations | Mutable Unity authoring data. |
| [`FormationSlotDefinition`](formations.md#formationslotdefinition) | class | Formations | Mutable Unity authoring data for one seat in a formation preset: where a combatant stands, which way it faces, how it sorts against the other seats, where a step-in beat leads, and... |
| [`FormationVfxAnchorDefinition`](formations.md#formationvfxanchordefinition) | class | Formations | Mutable Unity authoring data for one named point on a formation slot that a presentation beat can target instead of the slot itself. |
| [`FormationViewport`](formations.md#formationviewport) | struct | Formations | The screen-space rectangle a formation is projected into, in pixels, with the origin at `Left`/`Bottom` and Y increasing upward. |
| [`ProjectedFormationPoint`](formations.md#projectedformationpoint) | struct | Formations | A formation point after projection, in the pixel space of the `FormationViewport` it was fitted into. |
| [`BattleSkinDefaults`](skinning-and-appearance.md#battleskindefaults) | class | Skinning and appearance | The shipped skins, defined in code rather than as serialized assets. |
| [`BattleSkinPreset`](skinning-and-appearance.md#battleskinpreset) | class | Skinning and appearance | Every value the battle interface draws itself with, in one asset. |
| [`CompiledBattleSkin`](skinning-and-appearance.md#compiledbattleskin) | class | Skinning and appearance | The immutable skin the HUD reads. |
| [`SkinAnchor`](skinning-and-appearance.md#skinanchor) | enum | Skinning and appearance | Where a HUD region attaches inside the safe area. |
| [`SkinBarTokens`](skinning-and-appearance.md#skinbartokens) | struct | Skinning and appearance | A value bar: health, shield, resource, cast, or gauge. |
| [`SkinEasing`](skinning-and-appearance.md#skineasing) | enum | Skinning and appearance | The easing curve applied to a skinned transition. |
| [`SkinFillMode`](skinning-and-appearance.md#skinfillmode) | enum | Skinning and appearance | How a skinned surface fills its rectangle. |
| [`SkinFloatingNumberTokens`](skinning-and-appearance.md#skinfloatingnumbertokens) | struct | Skinning and appearance | Rise-and-fade numbers for damage, healing, and shields. |
| [`SkinLayoutProfile`](skinning-and-appearance.md#skinlayoutprofile) | enum | Skinning and appearance | Which band composition a layout is authored for. |
| [`SkinMaterialPool`](skinning-and-appearance.md#skinmaterialpool) | class | Skinning and appearance | Reference-counted material pool for skinned surfaces, owned by a component rather than by static state. |
| [`SkinMotionTokens`](skinning-and-appearance.md#skinmotiontokens) | struct | Skinning and appearance | Transition timings. |
| [`SkinPaletteTokens`](skinning-and-appearance.md#skinpalettetokens) | struct | Skinning and appearance | The semantic colour roles a skin assigns once and reuses everywhere. |
| [`SkinRegionStretch`](skinning-and-appearance.md#skinregionstretch) | enum | Skinning and appearance | How a HUD region behaves on each axis: pinned at its authored size, or stretched to the full width or height of the safe area. |
| [`SkinRegionTokens`](skinning-and-appearance.md#skinregiontokens) | struct | Skinning and appearance | Where one HUD region sits. |
| [`SkinShape`](skinning-and-appearance.md#skinshape) | enum | Skinning and appearance | The silhouette a skinned surface draws. |
| [`SkinStagePresenceTokens`](skinning-and-appearance.md#skinstagepresencetokens) | struct | Skinning and appearance | How the stage stages its combatants: the falloff between depth ranks, the contact shadow every body stands on, and the one warm key light. |
| [`SkinStatusPipTokens`](skinning-and-appearance.md#skinstatuspiptokens) | struct | Skinning and appearance | The status pip strip drawn above a combatant. |
| [`SkinSurfaceGraphic`](skinning-and-appearance.md#skinsurfacegraphic) | class | Skinning and appearance | Draws one `SkinSurfaceTokens` as a uGUI graphic through the TurnGauge skinned-surface shader. |
| [`SkinSurfaceTokens`](skinning-and-appearance.md#skinsurfacetokens) | struct | Skinning and appearance | Fill, stroke, and glow for one skinned surface. |
| [`SkinTargetingTokens`](skinning-and-appearance.md#skintargetingtokens) | struct | Skinning and appearance | How a target pick is expressed. |
| [`SkinTypographyTokens`](skinning-and-appearance.md#skintypographytokens) | struct | Skinning and appearance | Type sizing and treatment. |
| [`BattleEventNarrator`](interface-and-widgets.md#battleeventnarrator) | class | Interface and widgets | Turns one battle event into a sentence a player can read. |
| [`BattleNumberFormat`](interface-and-widgets.md#battlenumberformat) | class | Interface and widgets | Turns the simulation's fixed-point types into player-facing text. |
| [`BattleUiCommandChoice`](interface-and-widgets.md#battleuicommandchoice) | struct | Interface and widgets | A player-chosen command the driver (not the UI) will submit. |
| [`BattleUiRoot`](interface-and-widgets.md#battleuiroot) | class | Interface and widgets | The battle interface. |
| [`DecisionOptions`](interface-and-widgets.md#decisionoptions) | class | Interface and widgets | The complete set of legal command shapes for one pending decision: filtered granted skills plus whether concession is offered. |
| [`DecisionShapeCompiler`](interface-and-widgets.md#decisionshapecompiler) | class | Interface and widgets | Pure compiler of legal command shapes from a snapshot and compiled catalog. |
| [`DisplayStringTable`](interface-and-widgets.md#displaystringtable) | class | Interface and widgets | A non-authoritative map from stable id to display text. |
| [`DisplayStringTableProvider`](interface-and-widgets.md#displaystringtableprovider) | class | Interface and widgets | Serialized, project-owned source of non-authoritative display labels. |
| [`FeedbackLogView`](interface-and-widgets.md#feedbacklogview) | class | Interface and widgets | The rolling battle log. |
| [`ResultBannerView`](interface-and-widgets.md#resultbannerview) | class | Interface and widgets | The terminal result banner. |
| [`SafeAreaFitter`](interface-and-widgets.md#safeareafitter) | class | Interface and widgets | Insets a `RectTransform` to the device safe area so HUD regions never land under a notch, a punch-hole camera, or a home indicator. |
| [`SkillCommandShape`](interface-and-widgets.md#skillcommandshape) | class | Interface and widgets | One legal skill command shape offered to the pending actor. |
| [`SkillTitleView`](interface-and-widgets.md#skilltitleview) | class | Interface and widgets | The skill title card: the name of what is being performed, announced as it happens and gone again a moment later. |
| [`SkillTrayView`](interface-and-widgets.md#skilltrayview) | class | Interface and widgets | The command tray offered to a pending human actor: one button per legal skill shape plus concede. |
| [`SkinnedTokenPlate`](interface-and-widgets.md#skinnedtokenplate) | class | Interface and widgets | The floating plate above one combatant: name, health, shield, cast progress, scheduler gauge, and status pips. |
| [`SkinnedValueBar`](interface-and-widgets.md#skinnedvaluebar) | class | Interface and widgets | A skinned value bar: track, an optional trailing ghost showing the value just lost, the live fill, and an optional numeric readout. |
| [`SkinnedWidgetFactory`](interface-and-widgets.md#skinnedwidgetfactory) | class | Interface and widgets | Builds the skinned uGUI primitives the HUD is assembled from. |
| [`StatusRosterView`](interface-and-widgets.md#statusrosterview) | class | Interface and widgets | The combatant roster: one row per combatant with name, health bar, shield readout, and status count. |
| [`TargetPickerView`](interface-and-widgets.md#targetpickerview) | class | Interface and widgets | The target picker: one button per combatant the chosen skill may legally hit, plus confirm and back. |
| [`TargetShape`](interface-and-widgets.md#targetshape) | struct | Interface and widgets | The display-only shape of a skill's target request, taken from the compiled target contract. |
| [`TimelineStripView`](interface-and-widgets.md#timelinestripview) | class | Interface and widgets | The turn-order rail: one chip per upcoming actor, left to right, with the actor about to act raised, accented, and marked NOW. |
| [`TooltipData`](interface-and-widgets.md#tooltipdata) | struct | Interface and widgets | A passive tooltip value computed by the DRIVER through the public preview surface (`BattleFormulaService.Preview` / `PreviewStatusApplication`, `FormulaPreview`, and `IEffectResolv... |
| [`TooltipPanelView`](interface-and-widgets.md#tooltippanelview) | class | Interface and widgets | The skill tooltip: cost, timing, target shape, and the driver-computed preview figures. |
| [`TransportBarView`](interface-and-widgets.md#transportbarview) | class | Interface and widgets | Scenario picker, seed field, and playback controls, drawn with the skin. |
| [`UiPortraitFacing`](interface-and-widgets.md#uiportraitfacing) | struct | Interface and widgets | Describes the direction painted into a portrait and the direction the presentation wants that portrait to face. |
| [`UiStatusEntry`](interface-and-widgets.md#uistatusentry) | struct | Interface and widgets | One combatant's surfaced status-panel row. |
| [`UiTimelineEntry`](interface-and-widgets.md#uitimelineentry) | struct | Interface and widgets | One chip on the turn-order rail: who acts, whose side they are on, how much of them is left, and whether they are still standing. |
| [`BattlePresenter`](stage-and-tokens.md#battlepresenter) | class | Stage and tokens | The pure presentation consumer. |
| [`BattleStage2D`](stage-and-tokens.md#battlestage2d) | class | Stage and tokens | A neutral 2D battle stage. |
| [`BattleStageBackdrop`](stage-and-tokens.md#battlestagebackdrop) | class | Stage and tokens | Optional background blur for the perform moment. |
| [`BattleStageBloom`](stage-and-tokens.md#battlestagebloom) | class | Stage and tokens | Optional stage bloom and vignette. |
| [`BattleStageFrame`](stage-and-tokens.md#battlestageframe) | class | Stage and tokens | Controls where the battle stage sits on screen and how large it is. |
| [`BattleStageInformationBank`](stage-and-tokens.md#battlestageinformationbank) | class | Stage and tokens | A side rail. |
| [`BattleStageInformationBankSide`](stage-and-tokens.md#battlestageinformationbankside) | enum | Stage and tokens | Which side of the information rail receives a team. |
| [`BattleStageInformationBanks`](stage-and-tokens.md#battlestageinformationbanks) | class | Stage and tokens | Optional, renderer-independent composition information for the two side rails. |
| [`BattleStageInformationEntry`](stage-and-tokens.md#battlestageinformationentry) | struct | Stage and tokens | One combatant retained by a side bank, including overflow entries. |
| [`BattleStageInformationSide`](stage-and-tokens.md#battlestageinformationside) | struct | Stage and tokens | Maps a caller-owned team identity to a rail side without naming assumptions. |
| [`BeatDeriver`](stage-and-tokens.md#beatderiver) | class | Stage and tokens | Pure event-to-beat derivation. |
| [`CombatantTokenView`](stage-and-tokens.md#combatanttokenview) | class | Stage and tokens | A neutral 2D token view for one combatant. |
| [`PresentationBeat`](stage-and-tokens.md#presentationbeat) | class | Stage and tokens | One immutable presentation beat: the event context plus the resolved recipe. |
| [`PresentationBeatContext`](stage-and-tokens.md#presentationbeatcontext) | struct | Stage and tokens | The non-authoritative, immutable data a beat needs, extracted entirely from one gameplay event's property set. |
| [`PresentationStagePreset`](stage-and-tokens.md#presentationstagepreset) | class | Stage and tokens | Closed, neutral presentation content for a battle stage. |
| [`PresenterBinding`](stage-and-tokens.md#presenterbinding) | class | Stage and tokens | The explicit dependency bundle a driver hands to a `BattlePresenter`. |
| [`StageAnimationBinding`](stage-and-tokens.md#stageanimationbinding) | class | Stage and tokens | Authored key to neutral source/target pulse binding. |
| [`StageAnimationSource`](stage-and-tokens.md#stageanimationsource) | enum | Stage and tokens | Where a neutral sample animation is anchored. |
| [`StageAudioBinding`](stage-and-tokens.md#stageaudiobinding) | class | Stage and tokens | Authored key to a one-shot audio clip. |
| [`StageFrameMode`](stage-and-tokens.md#stageframemode) | enum | Stage and tokens | How the stage rectangle is derived from the screen. |
| [`StagePresentationPlayback`](stage-and-tokens.md#stagepresentationplayback) | class | Stage and tokens | Owns a preset's isolated presentation copies and transient stage effects. |
| [`StageVfxBinding`](stage-and-tokens.md#stagevfxbinding) | class | Stage and tokens | Authored key to a stage VFX prototype. |
| [`TargetPreviewView`](stage-and-tokens.md#targetpreviewview) | class | Stage and tokens | Draws what a skill is about to hit, on the stage, before the player commits. |
| [`TargetingReticleView`](stage-and-tokens.md#targetingreticleview) | class | Stage and tokens | The cursor that lives on one candidate: a marker hanging over whoever is currently pointed at, with that candidate's position in the list beside it. |
| [`BackdropBlurPerformModule`](the-perform-moment.md#backdropblurperformmodule) | class | The perform moment | Pulls focus for the whole perform: the background goes out of focus as the skill winds up and comes back as it closes. |
| [`BloomPulsePerformModule`](the-perform-moment.md#bloompulseperformmodule) | class | The perform moment | Adds a burst of bloom on impact, over whatever the optional bloom component is resting at. |
| [`BodyShakePerformModule`](the-perform-moment.md#bodyshakeperformmodule) | class | The perform moment | Jolts the combatant that was struck, so a hit reads on the body as well as in the numbers. |
| [`CameraShakePerformModule`](the-perform-moment.md#camerashakeperformmodule) | class | The perform moment | Shakes the battle camera when a phase asks for it. |
| [`CameraZoomPerformModule`](the-perform-moment.md#camerazoomperformmodule) | class | The perform moment | Pushes the camera in through the impact and releases it afterwards. |
| [`FocusPerformModule`](the-perform-moment.md#focusperformmodule) | class | The perform moment | Dims everyone not taking part, so the eye goes to the combatants the action concerns. |
| [`IPerformBeatModule`](the-perform-moment.md#iperformbeatmodule) | interface | The perform moment | One step of the perform moment: the announcement, the focus pull, the shake, the return, or anything a project invents. |
| [`PerformBeatPhase`](the-perform-moment.md#performbeatphase) | enum | The perform moment | The parts of one impact, in the order a player reads them. |
| [`PerformFeelPreset`](the-perform-moment.md#performfeelpreset) | class | The perform moment | One asset holding how the perform moment feels: how long the skill title holds, how far the camera pushes in, how hard the impact hits, how the world behind the action recedes. |
| [`PerformModuleBase`](the-perform-moment.md#performmodulebase) | class | The perform moment | Shared plumbing for the shipped modules: a feel preset that is never null, and a decaying timer, which is the shape almost every piece of juice takes. |
| [`PerformPhaseContext`](the-perform-moment.md#performphasecontext) | struct | The perform moment | Everything a perform module is told about the phase it is reacting to. |
| [`SkillAnnouncementPerformModule`](the-perform-moment.md#skillannouncementperformmodule) | class | The perform moment | Puts the performed skill's name on screen as the action opens. |
| [`VignettePulsePerformModule`](the-perform-moment.md#vignettepulseperformmodule) | class | The perform moment | Closes the frame in on impact by pulsing the optional stage vignette, then eases it back to the strength the component is resting at. |
| [`BuiltInAnimationAdapter`](presentation-adapters-and-recipes.md#builtinanimationadapter) | class | Presentation adapters and recipes | Neutral built-in animation adapter. |
| [`BuiltInAudioAdapter`](presentation-adapters-and-recipes.md#builtinaudioadapter) | class | Presentation adapters and recipes | Neutral built-in audio adapter. |
| [`BuiltInPoolAdapter`](presentation-adapters-and-recipes.md#builtinpooladapter) | class | Presentation adapters and recipes | Simple keyed GameObject pool. |
| [`BuiltInVfxAdapter`](presentation-adapters-and-recipes.md#builtinvfxadapter) | class | Presentation adapters and recipes | Neutral built-in VFX adapter. |
| [`FloatingNumberStyle`](presentation-adapters-and-recipes.md#floatingnumberstyle) | enum | Presentation adapters and recipes | Floating-number presentation style; purely cosmetic. |
| [`IAnimationAdapter`](presentation-adapters-and-recipes.md#ianimationadapter) | interface | Presentation adapters and recipes | Plays a keyed animation for a beat phase. |
| [`IAudioAdapter`](presentation-adapters-and-recipes.md#iaudioadapter) | interface | Presentation adapters and recipes | Plays a keyed one-shot sound. |
| [`IPoolAdapter`](presentation-adapters-and-recipes.md#ipooladapter) | interface | Presentation adapters and recipes | Keyed instance pool for token views, floating numbers, and pooled VFX. |
| [`IPoolPrototypeQuery`](presentation-adapters-and-recipes.md#ipoolprototypequery) | interface | Presentation adapters and recipes | An optional capability a pool may add: answering whether it holds a prototype for a key, without acquiring one. |
| [`IVfxAdapter`](presentation-adapters-and-recipes.md#ivfxadapter) | interface | Presentation adapters and recipes | Plays a keyed one-shot visual effect at the cue position. |
| [`PresentationBeatSpec`](presentation-adapters-and-recipes.md#presentationbeatspec) | class | Presentation adapters and recipes | One of the three fixed beats (In / Impact / Out) of a recipe. |
| [`PresentationCue`](presentation-adapters-and-recipes.md#presentationcue) | struct | Presentation adapters and recipes | Immutable spatial context handed to a visual adapter. |
| [`PresentationLog`](presentation-adapters-and-recipes.md#presentationlog) | class | Presentation adapters and recipes | Non-authoritative, log-once warning ledger shared by the presenter and its adapters. |
| [`PresentationRecipeDefinition`](presentation-adapters-and-recipes.md#presentationrecipedefinition) | class | Presentation adapters and recipes | A stable-id presentation recipe (In / Impact / Out beats) authored as a B4-style ScriptableObject. |
| [`PresentationRecipeSet`](presentation-adapters-and-recipes.md#presentationrecipeset) | class | Presentation adapters and recipes | An explicit, ordered list of presentation recipes. |
| [`PresentationSelectorKind`](presentation-adapters-and-recipes.md#presentationselectorkind) | enum | Presentation adapters and recipes | How a recipe selector narrows an event to a specific mechanic. |
| [`PresentationVfxAnchorKind`](presentation-adapters-and-recipes.md#presentationvfxanchorkind) | enum | Presentation adapters and recipes | Where a beat's VFX anchors, resolved through the compiled slot. |
| [`IReplayMigration`](replay.md#ireplaymigration) | interface | Replay | One step of a replay upgrade: it takes the bytes of a replay written in `FromFormatVersion` and returns the same replay written in `ToFormatVersion`. |
| [`ReplayDivergenceHashKind`](replay.md#replaydivergencehashkind) | enum | Replay | Which pair of hashes disagreed when a replay diverged. |
| [`ReplayEnvelope`](replay.md#replayenvelope) | class | Replay | A complete, portable recording of one battle: the contract profile it ran under, the hashed compiled content and start request, the RNG seed, every recorded command, and the checkp... |
| [`ReplayExecutionResult`](replay.md#replayexecutionresult) | class | Replay | The verdict of one replay run: whether the recording reproduced, the state the run ended on, and, when it did not reproduce, the exact command or checkpoint it stopped at and the h... |
| [`ReplayExecutor`](replay.md#replayexecutor) | class | Replay | Re-runs a recorded battle from its seed and its recorded commands and reports whether it reproduced. |
| [`ReplayMigrationChain`](replay.md#replaymigrationchain) | class | Replay | A validated set of single-version `IReplayMigration` steps that lifts replay bytes from the format version they were written in up to a newer one, feeding each step's output into t... |
| [`ReplayMigrationResult`](replay.md#replaymigrationresult) | class | Replay | The outcome of one migration step, or of a whole `ReplayMigrationChain` run: either the rewritten replay bytes or the diagnostic explaining the refusal, never both. |
| [`ReplayReadResult`](replay.md#replayreadresult) | class | Replay | The outcome of parsing a replay. |
| [`ReplaySerializer`](replay.md#replayserializer) | class | Replay | Writes and reads the portable replay document that carries a battle's compiled content, start request, seed, and recorded command history as UTF-8 JSON. |
| [`ReplayWriteException`](replay.md#replaywriteexception) | class | Replay | Thrown when a replay cannot be written out: its contract profile is unsupported or disagrees with the content it embeds, a field that profile requires is absent, the recorded histo... |
| [`AnalysisDiagnosticIds`](analysis-and-balancing.md#analysisdiagnosticids) | class | Analysis and balancing | Permanent diagnostic identifiers for analysis batch contract 1. |
| [`AnalysisLimits`](analysis-and-balancing.md#analysislimits) | class | Analysis and balancing | Structural limits for analysis batch contract 1. |
| [`BatchExport`](analysis-and-balancing.md#batchexport) | class | Analysis and balancing | Deterministic CSV and JSON text generation for batch results. |
| [`BatchOutcomeKind`](analysis-and-balancing.md#batchoutcomekind) | enum | Analysis and balancing | The recorded stop reason of one batch battle. |
| [`BatchSeedPlan`](analysis-and-balancing.md#batchseedplan) | class | Analysis and balancing | An immutable deduplicated ascending seed list. |
| [`BattleBatchAggregate`](analysis-and-balancing.md#battlebatchaggregate) | class | Analysis and balancing | The deterministic single-threaded ordered reduction over the sorted records of one completed batch. |
| [`BattleBatchLimits`](analysis-and-balancing.md#battlebatchlimits) | class | Analysis and balancing | Per-battle stopping bounds. |
| [`BattleBatchRequest`](analysis-and-balancing.md#battlebatchrequest) | class | Analysis and balancing | The complete immutable input of one Monte Carlo batch. |
| [`BattleBatchResult`](analysis-and-balancing.md#battlebatchresult) | class | Analysis and balancing | The complete immutable result of one batch execution. |
| [`BattleBatchRunner`](analysis-and-balancing.md#battlebatchrunner) | class | Analysis and balancing | The deterministic scripted AI-versus-AI Monte Carlo runner. |
| [`BattleOutcomeRecord`](analysis-and-balancing.md#battleoutcomerecord) | class | Analysis and balancing | The immutable outcome of one batch battle. |
| [`SingleBattleReproduction`](analysis-and-balancing.md#singlebattlereproduction) | class | Analysis and balancing | A single-seed rerun derived by the exact batch per-battle algorithm plus the strict replay bytes captured from the same engine. |
| [`TeamWinCount`](analysis-and-balancing.md#teamwincount) | class | Analysis and balancing | One winning team and how many batch records it won. |
| [`CanonicalBattleSerializer`](numerics-and-determinism.md#canonicalbattleserializer) | class | Numerics and determinism | Encodes and decodes battle state as a canonical byte stream. |
| [`Chance64`](numerics-and-determinism.md#chance64) | struct | Numerics and determinism | A deterministic probability value where 1,000,000 raw units equal 100%. |
| [`DeterministicRng`](numerics-and-determinism.md#deterministicrng) | struct | Numerics and determinism | The simulation's random source: a 128-bit xorshift-rotate generator over four 32-bit words, computed with integer arithmetic only, so one seed yields one sequence on every platform... |
| [`Diagnostic`](numerics-and-determinism.md#diagnostic) | struct | Numerics and determinism | One reported failure or warning: a stable id plus optional free-text detail. |
| [`Fixed64`](numerics-and-determinism.md#fixed64) | struct | Numerics and determinism | A signed fixed-point number carrying four decimal places, stored as a 64-bit integer in which 10,000 raw units make 1.0. |
| [`FrozenList`](numerics-and-determinism.md#frozenlist) | class | Numerics and determinism | A list that copies what it is given once and then offers no way to change it, used throughout compiled content, snapshots, and events wherever a collection crosses a public boundar... |
| [`Sha256Digest`](numerics-and-determinism.md#sha256digest) | struct | Numerics and determinism | An immutable 32-byte SHA-256 digest, used to fingerprint a canonical record so two runs can be compared for divergence. |
| [`StableId`](numerics-and-determinism.md#stableid) | struct | Numerics and determinism | The identifier every piece of content, state, and event in the simulation is named by: 1 to 128 characters drawn from a-z, 0-9, and the three punctuation characters '.', '_' and '-... |
| [`BattleSkinBrowserWindow`](editor-tools.md#battleskinbrowserwindow) | class | Editor tools | Browse the shipped skins, preview them with the real shader, and turn any of them into an editable asset in one click. |
| [`CombatStudioSampleBuilder`](editor-tools.md#combatstudiosamplebuilder) | class | Editor tools | Creates editable starter profiles and native view prefabs using Unity's asset APIs. |
| [`TurnGaugeDemoBootstrap.AudioArtBinding`](other.md#audioartbinding) | class | Other | Binds a recipe audio key (an sfx-* clip name) to art. |
| [`BattleRuntimeController.AudioBinding`](other.md#audiobinding) | class | Other | Maps one presentation audio key to a Unity audio clip. |
| [`BattleCancelRelay`](other.md#battlecancelrelay) | class | Other | Routes the active input module's cancel event without depending on a particular input package. |
| [`BattleFeedbackLayout`](other.md#battlefeedbacklayout) | class | Other | Computes a deterministic clear rectangle for presentation feedback. |
| [`BattleLayoutIdentity`](other.md#battlelayoutidentity) | enum | Other | Visual family used for starter palettes and default stage reservations. |
| [`BattlePresentationLabel`](other.md#battlepresentationlabel) | class | Other | One display text override owned by a presentation profile. |
| [`BattlePresentationProfile`](other.md#battlepresentationprofile) | class | Other | Authored references only. |
| [`BattleProfileCatalog`](other.md#battleprofilecatalog) | class | Other | Owns the partial runtime catalog required by a presentation profile. |
| [`BattleRulesPreset`](other.md#battlerulespreset) | enum | Other | Choice of Action Order rounds or paused ATB when deriving a profile's runtime catalog. |
| [`BattleRuntimeCheckpoint`](other.md#battleruntimecheckpoint) | class | Other | Persistable battle restore point. |
| [`BattleRuntimeController`](other.md#battleruntimecontroller) | class | Other | Coordinates authored presentation profiles, runtime views and optional stage presentation. |
| [`BattleRuntimeEndReason`](other.md#battleruntimeendreason) | enum | Other | Why a normally driven battle stopped advancing. |
| [`BattleRuntimeEndedEvent`](other.md#battleruntimeendedevent) | class | Other | Payload raised when driving reaches a clean end. |
| [`BattleRuntimeEventsEvent`](other.md#battleruntimeeventsevent) | class | Other | Payload raised for a non-empty event batch. |
| [`BattleRuntimeFailedEvent`](other.md#battleruntimefailedevent) | class | Other | Payload raised for fail-closed runtime failures. |
| [`BattleRuntimeFailure`](other.md#battleruntimefailure) | enum | Other | Typed reasons a facade operation can fail without throwing. |
| [`BattleRuntimeHumanControlRequirement`](other.md#battleruntimehumancontrolrequirement) | enum | Other | Optional fail-closed check over the control kinds authored into an encounter. |
| [`BattleRuntimeOperationResult`](other.md#battleruntimeoperationresult) | class | Other | Common typed result returned by controller operations. |
| [`BattleRuntimePacing`](other.md#battleruntimepacing) | enum | Other | How the controller decides when the battle clock may advance. |
| [`BattleRuntimeSeedPolicy`](other.md#battleruntimeseedpolicy) | enum | Other | How the no-argument StartBattle operation chooses its seed. |
| [`BattleRuntimeSnapshotCause`](other.md#battleruntimesnapshotcause) | enum | Other | Why a snapshot was published through SnapshotChanged. |
| [`BattleRuntimeSnapshotEvent`](other.md#battleruntimesnapshotevent) | class | Other | Payload raised whenever the authoritative snapshot changes. |
| [`BattleRuntimeStartedEvent`](other.md#battleruntimestartedevent) | class | Other | Payload raised when a battle starts or is restored. |
| [`BattleRuntimeState`](other.md#battleruntimestate) | enum | Other | The runtime facade's externally visible lifecycle. |
| [`BattleRuntimeUnityEvent`](other.md#battleruntimeunityevent) | class | Other | Parameterless inspector event paired with the typed C# events. |
| [`BattleRuntimeValueResult`](other.md#battleruntimevalueresult) | class | Other | An operation result that also returns an immutable value. |
| [`BattleStageBounds`](other.md#battlestagebounds) | struct | Other | A presentation-only rectangle in normalized screen space, with a bottom-left origin. |
| [`BattleTheme`](other.md#battletheme) | class | Other | Serializable visual values copied by views before they render. |
| [`BattleUiCommandTranslationResult`](other.md#battleuicommandtranslationresult) | class | Other | Typed result of translating a presentation choice into a command. |
| [`BattleUiCommandTranslator`](other.md#battleuicommandtranslator) | class | Other | Turns a UI choice into the exact command shape the engine expects. |
| [`BattleUiTechnology`](other.md#battleuitechnology) | enum | Other | Native UI backend required by a profile's view prefab. |
| [`BattleViewAction`](other.md#battleviewaction) | class | Other | A legal action and the candidate IDs supplied by its actual resolver. |
| [`BattleViewBehaviour`](other.md#battleviewbehaviour) | class | Other | Unity lifecycle shell. |
| [`BattleViewCombatant`](other.md#battleviewcombatant) | class | Other | Immutable, renderer-independent information shown for one combatant. |
| [`BattleViewCommand`](other.md#battleviewcommand) | struct | Other | Immutable command choice forwarded for authoritative validation. |
| [`BattleViewIntent`](other.md#battleviewintent) | struct | Other | A UI gesture; the host still validates the resulting command. |
| [`BattleViewIntentKind`](other.md#battleviewintentkind) | enum | Other | Interaction intents understood by a battle view session. |
| [`BattleViewProjection`](other.md#battleviewprojection) | class | Other | The single snapshot-to-UI projection for every native or customer renderer. |
| [`BattleViewRoster`](other.md#battleviewroster) | class | Other | Pure grouping helpers for immutable presentation rosters. |
| [`BattleViewSession`](other.md#battleviewsession) | class | Other | Shared interaction state survives visual tree reconstruction. |
| [`BattleViewState`](other.md#battleviewstate) | class | Other | A complete read-only view; contains no scene objects or authority to change combat. |
| [`CustomMechanicsRegistryProvider`](other.md#custommechanicsregistryprovider) | class | Other | Adds the sample shield effect and lowest-health ally target resolver to the built-in registry set used by authored battles and replay. |
| [`CustomShieldEffectResolver`](other.md#customshieldeffectresolver) | class | Other | Creates a shield equal to a configured fraction of missing health. |
| [`DemoIdleSheet`](other.md#demoidlesheet) | class | Other | Reads the sample character art, which ships as a grid of idle frames rather than as a single still so combatants breathe instead of standing frozen. |
| [`DisplayStringTableAsset`](other.md#displaystringtableasset) | class | Other | The shipped serialized string-table asset the demo driver supplies to the presenter (specification section 3: display text comes from an explicit table, never from compiled snapsho... |
| [`DisplayStringTableAsset.Entry`](other.md#entry) | class | Other | One stable-id-to-display-name pair. |
| [`ForecastRequest`](other.md#forecastrequest) | class | Other | The three caps that bound one `BattleForecast.Run` call: how far ahead it may look, and how much work and evidence it may collect before stopping. |
| [`ForecastResult`](other.md#forecastresult) | class | Other | Immutable outcome of one `BattleForecast.Run` call: where the lookahead stopped, the state and events of the throwaway clone it ran, and the non-authoritative evidence it produced. |
| [`ForecastStopReason`](other.md#forecaststopreason) | enum | Other | Why one `BattleForecast.Run` call stopped. |
| [`GeneratedUiText`](other.md#generateduitext) | class | Other | Marks adapter-owned text that participates in presentation themes. |
| [`IBattleFeedbackLayout`](other.md#ibattlefeedbacklayout) | interface | Other | Optional presentation-only reservation for feedback that must stay clear of the stage and its other information bands. |
| [`IBattlePointerBlocker`](other.md#ibattlepointerblocker) | interface | Other | Optional screen-space hit-test owned by a view. |
| [`IBattleStageInformationLayout`](other.md#ibattlestageinformationlayout) | interface | Other | Optional presentation-only choice to group combatant information beside the action stage. |
| [`IBattleStageLayout`](other.md#ibattlestagelayout) | interface | Other | Optional authored stage reservation. |
| [`IBattleView`](other.md#ibattleview) | interface | Other | Renderer-neutral contract for rendering state and forwarding intents. |
| [`IInteractiveBattleView`](other.md#iinteractivebattleview) | interface | Other | Optional interaction surface used by a world-space presentation bridge. |
| [`LowestHealthAllyTargetResolver`](other.md#lowesthealthallytargetresolver) | class | Other | Chooses the living targetable ally with the lowest health ratio. |
| [`TurnGaugeDemoBootstrap.ParticleArtBinding`](other.md#particleartbinding) | class | Other | Binds a recipe VFX key (a particle-* sprite name) to art. |
| [`TurnGaugeDemoBootstrap.SessionEndState`](other.md#sessionendstate) | enum | Other | Typed end-of-session states surfaced by the driver. |
| [`TargetCandidateQuery`](other.md#targetcandidatequery) | class | Other | Asks a skill's registered target resolver who it may legally hit right now, and whether one particular pick would be accepted. |
| [`TargetPreview`](other.md#targetpreview) | class | Other | Turns a resolver into the way its affected set should be shown, and a device into the way a pick should be expressed. |
| [`TargetTreatment`](other.md#targettreatment) | enum | Other | The visual language one target shape is previewed in. |
| [`TargetingPreset`](other.md#targetingpreset) | enum | Other | How a pick is expressed. |
| [`TurnGaugeDemoBootstrap.TokenArtBinding`](other.md#tokenartbinding) | class | Other | Binds a starter combatant definition id to its generated token sprite (the token-* art keys from the art manifest). |
| [`ToolkitBattleView`](other.md#toolkitbattleview) | class | Other | A replaceable UXML surface. |
| [`TurnGaugeDemoBootstrap`](other.md#turngaugedemobootstrap) | class | Other | The runtime demo driver (specification section 9). |
| [`UguiBattleView`](other.md#uguibattleview) | class | Other | Prefab-authored uGUI surface. |
| [`BattleRuntimeController.VfxBinding`](other.md#vfxbinding) | class | Other | Maps one presentation VFX key to an optional pooled prototype. |

</div>
