'use strict';

var modernMobile = angular.module('modernMobile', ['ui.bootstrap','ngRoute','transactionGridMod','historyTransactionMod']);

modernMobile.controller('modernMobileCtrl', ["$scope", "$http","$log","gridSvc","$rootScope", "transactionSvc","loginService",
	function($scope,$http,$log,gridSvc,$rootScope,transactionSvc,loginService) {
	$scope.transactionFile = "";
	$scope.upload = function(form) {
		console.log($scope.transactionFile);
		console.log(form);
		$rootScope.$emit("reload-grid-again");
	}
	
	$scope.readFileData = function(fileName) {
		var fileReader = new FileReader();
		fileReader.onload = function(event) {
			var data = event.target.result;
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
			description:'Hi!!',
			transactionDate:'1444565700',
			id:'s101'
		},
		requesterId:'+5211553788466'
	};

	$scope.individualTransaction1 = {
		to :{
			accountId:'+11234567899',
			amount:'1500.00',
			description:'Hi!!',
			transactionDate:'1444565500',
			id:'s100'
		},
		requesterId:'+5217222842257'
	};

	$scope.makeIndividualTransaction = function(val) {
		var data = [];
		if(val) {
			data.push($scope.individualTransaction1.to);
			transactionSvc.makeIndividualTransaction(data,$scope.individualTransaction1.requesterId);
		}
		else {
			data.push($scope.individualTransaction.to);
			transactionSvc.makeIndividualTransaction(data,$scope.individualTransaction.requesterId);
		}
		
	}

	$scope.init = function(user) {
		$scope.loggedInUser = user;
		loginService.getUserInfo({userId:user}).then(function(success,data){
			$scope.loggedInUserInfo = success.data;
			loginService.setUserInfo($scope.loggedInUserInfo);
		},function(error){
			console.log("Some Error has Occured");
		});
	}

	$scope.sideBars = [{'id':'dashBoard',displayName:'DashBoard',iconCls:'fa fa-dashboard fa-fw',link:''},
						{'id':'newLending',displayName:'New Transaction',iconCls:'fa fa-send fa-fw',link:''},
						{'id':'historyTransaction',displayName:'Past Transactions',iconCls:'fa fa-table fa-fw',link:'static/js/transactions/history.html'}];

	$scope.loadSideTab = function(index) {
		$scope.currentCentralPanel = $scope.sideBars[index];
		$scope.history = true;
		if(index != 2)
			$scope.history=false;
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
modernMobile.factory('loginService',['$http','$location',function($http,$location){

	var loginService;
	var userInfo = {};
	loginService = {
		'getUserInfo' : function(user) {

			// var host = $location.host();
			// var port = $location.port();
			// var url = "http://"+host;
			// if(typeof port !== "undefined" &&  port !== "")
			// 	url += ":"+port;
			var 
			url  = "/userInfo";
			return $http({
				'method':'POST',
				'data' : user,
				 'url' : url
			});
		},
		setUserInfo : function(user) {
			userInfo = user;
		},
		getInMemoryUserInfo : function(){
			return userInfo;
		}
	}
	return loginService;
}]);

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


