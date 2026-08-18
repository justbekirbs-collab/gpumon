EventScript_RepelWoreOff::
	msgbox Text_RepelWoreOff, MSGBOX_SIGN
	checkitem VAR_REPEL_LAST_USED, 1
	compare VAR_RESULT, TRUE
	goto_if_eq EventScript_AskUseRepel
	end

EventScript_AskUseRepel::
	msgbox Text_AskUseRepel, MSGBOX_YESNO
	compare VAR_RESULT, YES
	goto_if_eq EventScript_UseRepel
	end

EventScript_UseRepel::
	removeitem VAR_REPEL_LAST_USED, 1
	playse SE_REPEL
	copyvar VAR_0x8004, VAR_REPEL_LAST_USED
	callnative SetRepelStepCount
	msgbox Text_UsedRepel, MSGBOX_SIGN
	end

Text_RepelWoreOff::
	.string "REPEL's effect wore off…$"

Text_AskUseRepel::
	.string "Use another REPEL?$"

Text_UsedRepel::
	.string "Player used the REPEL.$"
