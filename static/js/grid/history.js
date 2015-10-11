/**
 * New node file
 */

var historyTransactionMod = angular.module("historyTransactionMod",[]);
var historyTransactionCtrl = historyTransactionMod.controller("historyTransactionCtrl",['$http','$scope',"historyGridConfigSvc","historyGridSvc",'loginService',
		function($http,$scope,historyGridConfigSvc,historyGridSvc,loginService){
		var columns = historyGridConfigSvc.getColDefs();
		var userInfo = loginService.getInMemoryUserInfo();

		var container = angular.element("#historySlickGrid");
		var options = {
			    enableCellNavigation: true,
			    enableColumnReorder: false,
			    forceFitColumns:true,
			    fullWidthRows:true,syncColumnCellResize:true
			  };
		var dataView = new Slick.Data.DataView();
		var data = $http({
			'method' : 'GET',
			'url' : 'getTransactions/' + userInfo.accountId
		}).then(function(success) {
			data = success.data;
			dataView.setItems(data);
	
		},function(error){

		});
		var grid = new Slick.Grid(container, dataView, columns, options);
		dataView.onRowCountChanged.subscribe(function (e, args) {
			  grid.updateRowCount();
			  grid.render();
			});

			dataView.onRowsChanged.subscribe(function (e, args) {
			  grid.invalidateRows(args.rows);
			  grid.render();
			});
	
}]);

var gridCfgService = gridModule.factory("historyGridConfigSvc",['formatters',function(formatters){
	return {
		"getColDefs" : function() {
			var columnDefs = [
	                  {name: "ID", field: "id",id:"id",sortable:true},
	                  {name: "Date", field: "transactionDate",id:"transactionDate",formatter:formatters.dateFormatter(),sortable:true },
	                  {name: "Amount", field: "amount",id:"amount",sortable:true,formatter:formatters.numberFormatter()},
	                  {name: "Description", field: "description",id:"description",sortable:true},
	                  {name: "Mobile Number", field: "toUser",id:"toUser",sortable:true}
	              ];
			return columnDefs; 
		}
	}
}]);

var gridService  = gridModule.factory("historyGridSvc",["gridConfigSvc","formatters",function(gridConfigSvc,formatters){
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
		},

		"numberFormatter" : function() {
			return function(row, cell, value, columnDef, dataContext) {
				return $filter('number')(value,2);
			}
		}
	}
	return formatters;
}])
