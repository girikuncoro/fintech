/**
 * New node file
 */

var gridModule = angular.module("transactionGridMod",[]);
var gridModule = gridModule.controller("transactionGridCtrl",['$http','$scope',"gridConfigSvc","gridSvc","$rootScope","transactionSvc",
     function($http,$scope,gridConfigSvc,gridService,$rootScope,transactionSvc){
		
		var columns = gridConfigSvc.getColDefs();
		var data = gridService.getData();
		var container = angular.element("#transaction-grid");
		var options = {
			    enableCellNavigation: true,
			    enableColumnReorder: false,
			    forceFitColumns:true,
			    fullWidthRows:true,syncColumnCellResize:true
			  };
		var dataView = new Slick.Data.DataView();
		var grid = new Slick.Grid(container, dataView, columns, options);
		dataView.onRowCountChanged.subscribe(function (e, args) {
			  grid.updateRowCount();
			  grid.render();
			});

			dataView.onRowsChanged.subscribe(function (e, args) {
			  grid.invalidateRows(args.rows);
			  grid.render();
			});
		dataView.setItems(data);
		
		var reloadGrid = function(event,data) {
			 var newData = gridService.parseData(data);
			 dataView.setItems(newData);
			
		 }

		 var saveTransactions = function(event) {
		 	var transactionData = dataView.getItems();
		 	transactionSvc.makeTransactions(transactionData);
		 }
 	
		 $rootScope.$on('reload-grid',reloadGrid);
		 $rootScope.$on('save-data',saveTransactions);
	
}]);

var gridCfgService = gridModule.factory("gridConfigSvc",['formatters',function(formatters){
	return {
		"getColDefs" : function() {
			var columnDefs = [
	                  {name: "Id", field: "id",id:"id",sortable:true},
	                  {name: "Date", field: "transactionDate",id:"transactionDate",formatter:formatters.dateFormatter(),sortable:true },
	                  {name: "Amount", field: "amount",id:"amount",sortable:true},
	                  {name: "Account Holder Name", field: "accountName",id:"accountName",sortable:true},
	                  {name: "Description", field: "description",id:"description",sortable:true},
	                  {name: "Mobile Number", field: "accountId",id:"accountId",sortable:true}
	              ];
			return columnDefs; 
		}
		
	}
}]);

var gridService  = gridModule.factory("gridSvc",["gridConfigSvc","formatters",function(gridConfigSvc,formatters){
	var gridService;
	var grid = {};
	var gridData = [];
	var fields = ['id','transactionDate','amount','accountName','description','accountId'];
	gridService = {
		"getGrid" : function() {
			var columnDefs = gridConfigSvc.getColDefs();
			var rowData = this.getData();
			grid = {
				'columnDefs': columnDefs,
				'rowData': rowData
			}
			return grid;
		},
		
		"refreshGridData" : function(data) {
			var parsedData = parseData(data);
			grid.rowData.length = 0;;
			parsedData.forEach(function(row) {
				grid.rowData.push(row);
			})
			console.log(grid.rowData);
			//grid.rowData = parsedData;
			grid.api.refreshView();
		},
		'parseData' : function(data) {
			console.log("parsing the data");
			//console.log(data);
			var allTextLines = data.split(/\r\n|\n/);
			var lines = [];
	        for (var i=1; i<allTextLines.length; i++) {
	            var data = allTextLines[i].split(',');
	                var tarr = {};
	                for (var j=0; j<data.length; j++) {
	                    tarr[fields[j]] = data[j];
	                }
	                lines.push(tarr);
	        }
	     // console.log(lines);
	      return lines;
		},
		"getData" : function() {
			return gridData;
		},

		"getTransactionData" : function() {

		}
 	}
	return gridService;
}]);

gridModule.factory('formatters',['$filter',function($filter){
	
	var formatters  = {
		
		"dateFormatter" : function() {
			return  function(row, cell, value, columnDef, dataContext) {
				return $filter('date')(value,'mediumDate');
			}
		}
	}
	return formatters;
}])
