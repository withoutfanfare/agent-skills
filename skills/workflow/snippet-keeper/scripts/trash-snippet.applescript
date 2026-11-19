-- Move one SnippetsLab snippet to the app's Bin, by UUID.
-- SnippetsLab has no AppleScript dictionary, so this opens the snippet by its
-- snippetslab:// link and uses Edit > Delete on the snippet list. It refuses
-- unless SnippetsLab is the front app and exactly one row is selected whose
-- title matches the one expected, so it can never delete the wrong snippet or
-- send anything to another app.
-- Usage: osascript trash-snippet.applescript <uuid> <exact title>

on frontName()
	tell application "System Events" to return name of (first process whose frontmost is true)
end frontName

on run argv
	if (count of argv) is not 2 then return "ABORT: usage: trash-snippet.applescript <uuid> <exact title>"
	set snippetUUID to item 1 of argv
	set expectedTitle to item 2 of argv

	tell application "SnippetsLab" to activate
	repeat 25 times
		if my frontName() is "SnippetsLab" then exit repeat
		delay 0.2
	end repeat
	if my frontName() is not "SnippetsLab" then return "ABORT: front app is " & my frontName()

	open location "snippetslab://snippet/" & snippetUUID
	delay 1

	tell application "System Events" to tell process "SnippetsLab"
		-- The main window, not "front window": a stray alert in front has no snippet list.
		set t to table 1 of scroll area 2 of splitter group 1 of (first window whose subrole is "AXStandardWindow")
		set sel to (rows of t whose selected is true)
		if (count of sel) is not 1 then return "ABORT: " & (count of sel) & " rows selected"
		set rowTitle to value of static text 1 of UI element 1 of item 1 of sel
		if rowTitle is not expectedTitle then return "ABORT: selected row is \"" & rowTitle & "\""

		set focused of t to true
		click UI element 1 of item 1 of sel
		delay 0.4
		if my frontName() is not "SnippetsLab" then return "ABORT: lost focus to " & my frontName()

		set mi to menu item "Delete" of menu "Edit" of menu bar 1
		-- The list is sometimes not ready for the first click; give it one more.
		if enabled of mi is false then
			delay 0.8
			click UI element 1 of item 1 of sel
			delay 0.6
			if my frontName() is not "SnippetsLab" then return "ABORT: lost focus to " & my frontName()
		end if
		if enabled of mi is false then return "ABORT: Edit > Delete is disabled"
		click mi
		delay 0.8
		return "OK: moved to Bin"
	end tell
end run
