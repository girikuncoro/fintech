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
		to : {
			accountId:'+5217222842257',
			amount:'500.00',
			description:'Hi!!'
		},
		requesterId:'+5211553788466'
	};

	$scope.individualTransaction1 = {
		to :{
			accountId:'+11234567899',
			amount:'1500.00',
			description:'Hi!!'
		},
		requesterId:'+5217222842257'
	};

	$scope.makeIndividualTransaction = function(val) {
		var data = [];
		if(val) {
			data.push($scope.individualTransaction1.to);
			transactionSvc.makeTransactions(data,$scope.individualTransaction1.requesterId);
		}
		else {
			data.push($scope.individualTransaction.to);
			transactionSvc.makeTransactions(data,$scope.individualTransaction.requesterId);
		}
		
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
			data['requesterId'] = '+11234567899';

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
		'makeIndividualTransaction' : function(data,requesterId) {
			var data = {};
			data['requests']  = data;
			data['requestType'] = 'Send';
			data['requesterId'] = requesterId;

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
