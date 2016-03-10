# Problem Format

This survey problem serves as an example for future problems. Each problem must be placed in its own directory, under the directory of its category (for organization). For the name of the folder, please use the ID of the problem (`pid`), which should be the name of the problem represented by lowercase words separated by dashes; don't include problem value. The program will automatically load the problems into the database.

## `problem.json`

The directory *must* contain a `problem.json`; this information will be loaded into the database. Refer to the following example:

```javascript
{
	"pid": "survey",					// required
	"title": "Survey",					// required
	"description": "Take our survey.",	// required - can use HTML
	"hint": "No hint!",					// optional - defaults to ""
	"category": "Miscellaneous",		// required
	"autogen": false,					// optional - defaults to false
	"programming": false,				// optional - defaults to false
	"value": 20,						// required - integer out of 800
	"bonus": 0,							// optional - defaults to 0; see below for details
	"threshold": 0,						// recommended - defaults to 0; see below for details
	"weightmap": { }					// recommended - defaults to {}
}
```

## `grader.py`

The directory must *also* contain a `grader.py`; this script must contain a `grade` function that takes in two parameters: `tid`, the team ID and `answer`, their attempted answer. The function must return a dict containing the following keys:

```python
{
	"correct": True # or False, indicating whether the answer is correct.
	"message": "Congratulations!" # a custom message for feedback on the website.
}
```

For the most part, checking in flags will simply be a matter of comparing strings. Make sure that the grader accepts the flag with or without `easyctf{}`. Here's an example grader that was taken from last year's Infinity Star problem:

```python
def grade(tid, answer):
	if answer.find("csrf_protection_would_probably_have_been_a_good_idea_:/") != -1:
		return { "correct": True, "message": "Indeed." }
	return { "correct": False, "message": "Nope, that's not quite right." }
```

You can copy-paste the above example into your grader and make any necessary adjustments. If you were wondering why we don't just compare strings, some problems may warrant a more complicated grader, like the problem H4SH3D from last year:

```python
import binascii

def compute(uinput):
	if len(uinput) > 32: return ""
	blen = 32
	n = blen - len(uinput) % blen
	if n == 0:
		n = blen
	pad = chr(n)
	ninput = uinput + pad * n
	r = ""
	for i in range(0, blen, 4):
		s = ninput[i:i+4]
		h = 0
		for j in range(len(s)):
			h = (h << 4) + ord(s[j])
			g = h & 4026531840
			if not(g == 0):
				h ^= g >> 24
			h &= ~g
		r += chr(h % 256)
	h = binascii.hexlify(bytes(r, 'Latin-1'))
	return h

def grade(tid, answer):
	if compute(answer) == compute("they_see_me_hashin_they_hatin"):
		return { "correct": True, "message": "They see me hashin' they hatin'" }
	return { "correct": False, "message": "Nope." }
```

## `static`

The directory *may* contain a `static` folder containing any static files that need to be served. This directory will be transferred to a static folder on the public site, so use `${static_folder}` to reference the static folder in links. For example, if your static folder contains a single `vuln.exe`, you might say

```html
Here is the <a href="${static_folder}/vuln.exe">vulnerable</a> binary.
```

The problem-loading script will expand these when the problems are loaded.

## Bonus Points

Bonus points encourage teams to finish solving a problem first. Rather than an array of three values like last year, we're going to have bonus-point templates. Each of the following integers is a code for a certain "template", and bonus points will be assigned accordingly.

| Code | 3rd | 2nd | 1st |
|------|-----|-----|-----|
| 0    | 0%  | 0%  | 0%  |
| 1    | 1%  | 2%  | 3%  |
| 2    | 1%  | 3%  | 5%  |
| 3    | 3%  | 5%  | 8%  |
| 4    | 6%  | 8%  | 10% |
| 5    | 8%  | 12% | 20% |

The table indicates how many percent bonus a team should receive if they solve a problem first, second, or third. Low problems such as the survey should not yield bonus points; only high-valued points should have bonus points in order to encourage teams t o solve them first.

## Problem Unlocking

Problem unlocking is managed through a mechanism that involves a threshold and weightmap. The weightmap is a dictionary mapping problem IDs to weight. The threshold is the minimum amount needed in order to unlock that particular problem. Take, for example, an abridged version of last year's Launch Code problem's JSON:

```javascript
{
	"pid": "launch-code",
	"threshold": 5,
	"weightmap":	{
		"php3": 1,
		"faster-math": 1,
		"biggerisbetter": 1,
		"cave-johnson": 1,
		"blackmesa": 1,
		"rsa3": 1,
		"yandere": 1,
		"rsi": 1,
		"adoughbee": 1,
		"infinity_star": 1
	}
}
```

That means in order to unlock Launch Code, a team would have to have solved five of the problems listed, since each problem has weight 1. It's also possible to add higher weights to a particular problem to promote solving that problem.