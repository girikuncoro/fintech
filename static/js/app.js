'use strict';

var API_CALL = '/api/v1.0/data/country/';

var modernMobile = angular.module('modernMobile', ['ui.bootstrap','ngRoute','transactionGridMod']);

modernMobile.controller('modernMobileCtrl', ["$scope", "$http","$log","gridSvc","$rootScope", function($scope,$http,$log,gridSvc,$rootScope) {
	$scope.transactionFile = "";
	$scope.upload = function(form) {
		console.log($scope.transactionFile);
		console.log(form);
		$rootScope.$emit("reload-grid-again");
	}
	
	$scope.readFileData = function(fileName) {
		var fileReader = new FileReader();
		fileReader.onload = function(event) {
			$scope.b
			var data = event.target.result;
			//console.log(data);
		//	gridSvc.refreshGridData(data);
			$rootScope.$emit("reload-grid",data);
		}
		fileReader.readAsText(fileName);
	}
	
	$scope.lendingTabs = [{'displayName' : 'Individual Transaction','templateName' : 'static/js/transactions/individualTransaction.html'},
	                      {'displayName' : 'Bulk Transaction','templateName' : 'static/js/transactions/bulkTransaction.html'}]			
	$scope.loadTab = function(index) {
		$scope.currentLendingTab = $scope.lendingTabs[index];
	}
}]);

modernMobile.config(['$interpolateProvider', function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
}]);

modernMobile.directive("fileHandler",[function() {
	return {
		require:"ngModel",
		restrict : "A",
		link : function($scope,element,attrs,ngModel) {
			element.bind("change",function(changeEvent){
				//console.log(changeEvent);
				var filename = changeEvent.target.files[0];
				$scope.readFileData(filename);
			})
		}
	}
}])
