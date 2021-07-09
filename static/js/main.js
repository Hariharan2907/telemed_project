function addColumn(tblId)
{
	var tblHeadObj = document.getElementById(tblId).tHead;
	for (var h=0; h<tblHeadObj.rows.length; h++) {
		var newTH = document.createElement('th');
		tblHeadObj.rows[h].appendChild(newTH);
		newTH.innerHTML = 'Cost '  + (tblHeadObj.rows[h].cells.length - 2)
	}

	var tblBodyObj = document.getElementById(tblId).tBodies[0];
	for (var i=0; i<tblBodyObj.rows.length; i++) {
		var newCell = tblBodyObj.rows[i].insertCell(-1);
		element = document.createElement("input");
        element.type = "number";
        element.name = "inter_costs" ;
        element.step = "any";
        newCell.appendChild(element);
	}
}

function deleteColumn(tblId)
{
	var allRows = document.getElementById(tblId).rows;
    
	for (var i=0; i<allRows.length; i++) {
		if (allRows[i].cells.length > 1) {
			allRows[i].deleteCell(-1);
		}
	}
}
function addRowToTable()
{
    var root = document.getElementById('input-table').getElementsByTagName('tbody')[0];
    var rows = root.getElementsByTagName('tr');
    
    var clone = cloneEl(rows[rows.length - 1]);
    
    root.appendChild(clone);

}
function cloneEl(el) {
    var clo = el.cloneNode(true);
    
    return clo;
}

function insertRow(tableID)
{
    var x = document.getElementById(tableID);
    var new_row = x.rows[1].cloneNode(true);
    var len = x.rows.length;
    new_row.cells[0].innerHTML = len;
  
    var inp1 = new_row.cells[1].getElementsByTagName('input')[0];
    inp1.id += len;
    inp1.value = '';
    var inp2 = new_row.cells[2].getElementsByTagName('input')[0];
    inp2.id += len;
    inp2.value = '';
    x.appendChild(new_row);
}

function addRows(){ 
	var table = document.getElementById('input-table');
	var rowCount = table.rows.length;
	var cellCount = table.rows[0].cells.length; 
	var row = table.insertRow(rowCount);
	for(var i =0; i <= cellCount; i++){
		var cell = 'cell'+i;
		cell = row.insertCell(i);
		var copycel = document.getElementById('col'+i).innerHTML;
		cell.innerHTML=copycel;

	}
}
function removeRow(oButton) {
    var tbl = document.getElementById('input-table');
    tbl.deleteRow(oButton.parentNode.parentNode.rowIndex);       // BUTTON -> TD -> TR.
}