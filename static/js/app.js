'use strict';

var modernMobile = angular.module('modernMobile', ['ui.bootstrap','ngRoute','transactionGridMod']);

modernMobile.controller('modernMobileCtrl', ["$scope", "$http","$log","gridSvc","$rootScope", "transactionSvc",
	function($scope,$http,$log,gridSvc,$rootScope,transactionSvc) {
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

	$scope.saveBulkTransaction = function() {
		$scope.$emit('save-data');
	}

	$scope.individualTransaction = {
		accountId:'+16073799018',
		amount:'500.00',
		description:'Hi!!'
	};

	$scope.makeIndividualTransaction = function() {
		var data = [];
		data.push($scope.individualTransaction);
		transactionSvc.makeTransactions(data);
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


modernMobile.factory('transactionSvc',['$http',function($http){
	var transactionSvc = {
		'makeTransactions' : function(transactionData) {
			var data = {};
			data['requests']  = transactionData;
			data['requestType'] = 'Send';
			data['requesterId'] = 'Abhishek';

			var url = "saveTransactions";
			console.log(transactionData);
			$http({
				'method' : 'POST',
				'data' : data,
				'url' : url,	
			}).then(function(success){

			},function(failure){

			})
		},
		'makeIndividualTransaction' : function(data) {
			var data = {};
			data['requests']  = data;
			data['requestType'] = 'Send';
			data['requesterId'] = 'Abhishek';

			var url = "saveTransactions";
			console.log(transactionData);
			$http({
				'method' : 'POST',
				'data' : data,
				'url' : url,	
			}).then(function(success){

			},function(failure){

			})
		}
	}

	return transactionSvc;
}]);
