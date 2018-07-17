let dragDialog = null;
let dragOffsetX = 0;
let dragOffsetY = 0;
document.addEventListener("mouseup", () => {
	if (dragDialog != null) {
		dragDialog = null;
		dragOffsetX = 0;
		dragOffsetY = 0;
	}
}, false);
document.addEventListener("mousemove", (evt) => {
	if (dragDialog != null) {
		dragDialog.style.top = Math.max(evt.screenY - dragOffsetY, 0) + "px";
		dragDialog.style.left = Math.max(evt.screenX - dragOffsetX, 0) + "px";
	}
}, false);

function showDialog(someElement) {
	let titleBar = create("div", {class: "dialog-titlebar"}, [
		create("button", "X", {class: "close-button", onclick:
			 "document.body.removeChild(this.parentNode.parentNode)"})
	]);
	titleBar.addEventListener("mousedown", (evt) => {
		dragDialog = evt.target.parentNode;
		dragOffsetX = evt.screenX - Number(evt.target.parentNode.style.left.replace("px", ""));
		dragOffsetY = evt.screenY - Number(evt.target.parentNode.style.top.replace("px", ""));
		document.body.removeChild(evt.target.parentNode);
		document.body.appendChild(evt.target.parentNode);
	}, false);
	let dialogWindow = create("div", {class: "dialog-window"}, [
		titleBar,
		create("div", {class: "dialog-content"}, [
			someElement
		])
	]);
	document.body.appendChild(dialogWindow);
	dialogWindow.style.top = ((document.documentElement.clientHeight - dialogWindow.clientHeight) / 2) + window.pageYOffset + "px";
	dialogWindow.style.left = ((document.documentElement.clientWidth - dialogWindow.clientWidth) / 2) + window.pageXOffset + "px";
}

var raw_data;
function exists(x) {
	if (x == null ||
	    typeof x == 'undefined' ||
	    x == ""
	) {
		return false;
	}
	return true;
}
function formatNames(names) {
	let formattedNames = "";
	for (let i = 0; i < names.length; i++) {
		if (i > 0) {formattedNames += ", ";}
		if (exists(names[i].firstName)) {
			formattedNames += names[i].firstName;
			if (exists(names[i].lastName)) { 
				formattedNames += " ";
			}
		}
		if (exists(names[i].lastName)) {
			formattedNames += names[i].lastName;
		}
	}
	return formattedNames;
}
function formatTribe(tribe) {
	if (tribe == "Unspecified") {
		return "";
	}
	return tribe;
}

function formatDate(someDate) {
	let year = "";
	let month = "";
	let day = "";
	if (exists(someDate.year)) { year = someDate.year; }
	if (exists(someDate.month)) { month = someDate.month; }
	if (exists(someDate.day)) { day = someDate.day; }
	if (!(exists(year) || exists(month) || exists(day))) {
		return "";
	}
	if (String(month).length == 1) { month = "0" + month; }
	if (String(day).length == 1) { day = "0" + day; }
	return [year, month, day].join("-");
}

function expandInformation(index) {
	item = raw_data[index]
	showDialog(create("div", [
		create("h2", formatNames(item.person.names), 
		       {style: "margin-top: 0px;"}),
		create("h3", "Document"),
		create("p", item.document.citation),
		create("p", item.document.stringLocation + ", " + 
		            item.document.nationalContext + " " + 
					item.document.colonyState + " - " + 
					formatDate(item.document.date)),
		create("h3", "Notes"),
		create("p", item.comments)
	]));
}

let imageFormatter = function(row, cell, value, columnDef, dataContext){
	return "<img src='" + value + "'/>";
};

let indexFormatter = function(row, cell, value, 
                              columnDef, dataContext) {
	return ("<img src='static/img/info.png' alt='VALUE' " +
	        "onclick='expandInformation(VALUE)' />")
	       .replace(/VALUE/g, value);
}

var dataView;
var grid;
var data = [
	{pic: "", id: "Johnny", name: "Johnny Saunders", 
	 documents: "Boston Times, Issues 54", events: "Baptism"},
	{pic: "",id: "Sammy", name: "Sammy Fletcher, Sammy Indigo", 
	 documents: "Old Time News", events: "Escape"},
	{pic: "",id: "Ronald", name: "Ronald Von Harrow", documents: "", 
	 events: "Marriage"},
];

var options = {
	enableCellNavigation: true,
	enableColumnSort: true,
	multiColumnSort: false,
	showHeaderRow: true,
	headerRowHeight: 30,
	rowHeight: 40,
	explicitInitialization: true,
	enableTextSelectionOnCells: true,
};
var columns = [
	{id: "persNumber",
	 name: "",
	 field: "persNumber",
	 width: 20,
	 formatter: indexFormatter,
	 sortable: false},
	{id: "names",
	 name: "Name",
	 field: "name",
	 width: 240,
	 sortable: true},
	{id: "date",
	 name: "Earliest record",
	 field: "date",
	 width: 100,
	 sortable: true},
	{id: "sex",
	 name: "Gender",
	 field: "sex",
	 width: 100,
	 sortable: true},
	{id: "typeKindOfEnslavement",
	 name: "Status",
	 field: "status",
	 width: 160,
	 sortable: true},
	{id: "race",
	 name: "Race",
	 field: "race",
	 width: 180,
	 sortable: true},
	{id: "tribe",
	 name: "Tribe / Nation",
	 field: "tribe",
	 width: 180,
	 sortable: true},
	{id: "origin",
	 name: "Origin",
	 field: "origin",
	 width: 180,
	 sortable: true},	
	{id: "vocation",
	 name: "Vocation",
	 field: "vocation",
	 width: 180,
	 sortable: true}
];
var columnFilters = {};

function filter(item) {
	for (var columnId in columnFilters) {
		if (columnId !== undefined 
		    && columnFilters[columnId] !== ""
		) {
			var c = grid.getColumns()[
				grid.getColumnIndex(columnId)
			];
			if (!item[c.field].toLowerCase().includes(
				columnFilters[columnId].toLowerCase())
			) { return false; }
		}
	}
	return true;
}