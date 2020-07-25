const fs = require("fs");

let settings = [];

for (let i = 0; i < 70; i++) {
	let choices = [];
	for (let j = 0; j < Math.floor(Math.random() * Math.floor(10)) + 1; j++) {
		choices.push({
			name: "Option" + j,
			weight: Math.floor(Math.random() * Math.floor(10)),
		});
	}
	settings.push({
		name: "Urne" + i,
		choices: choices,
	});
}

let data = JSON.stringify(settings, null, 2);
fs.writeFileSync("settings.json", data);
