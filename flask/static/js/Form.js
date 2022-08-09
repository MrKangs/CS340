var identifier = { 0:"exchangeID", 1:"txID", 2:"userID", 3:"fiatWalletID" ,4:"dogecoinWalletID"};


var data = JSON.parse(document.getElementById("query").innerHTML);

for (var i = 0; i<5; i++){
    if(identifier[i] in data){
        var value = i;
        break;
    }
}

switch(value){
    case 0:
        document.getElementById("exchangeID").value = data["exchangeID"];
        document.getElementById("exchangeID").readOnly = true;
        document.getElementById("fiatWalletID").value = data["fiatWalletID"];
        document.getElementById("dogecoinWalletID").value = data["dogecoinWalletID"];
        document.getElementById("orderTimestamp").value = data["orderTimestamp"];
        document.getElementById("orderTimestamp").readOnly = true;
        document.getElementById("amountFilled").value = data["amountFilled"];
        document.getElementById("orderDirection").value = data["orderDirection"];
        document.getElementById("orderType").value = data["orderType"];
        document.getElementById("orderPrice").value = data["orderPrice"];
        document.getElementById("title").innerText = "Update Exchange Order Record";
        break;
    case 1:
        document.getElementById("txID").value = data["txID"];
        document.getElementById("txID").readOnly = true;
        document.getElementById("txTimestamp").value = data["txTimestamp"];
        document.getElementById("txTimestamp").readOnly = true;
        document.getElementById("amount").value = data["amount"];
        document.getElementById("txDirection").value = data["txDirection"];
        document.getElementById("dogecoinWalletID").value = data["dogecoinWalletID"];
        document.getElementById("dogecoinWalletID").readOnly = true;
        document.getElementById("externalWalletAddress").value = data["externalWalletAddress"];
        document.getElementById("externalWalletAddress").readOnly = true;
        document.getElementById("txHash").value = data["txHash"];
        document.getElementById("txHash").readOnly = true;
        document.getElementById("title").innerText= "Update Dogecoin Transaction Record";
        break;
    case 2:
        document.getElementById("userID").value = data["userID"];
        document.getElementById("userID").readOnly = true;
        document.getElementById("firstName").value = data["firstName"];
        document.getElementById("lastName").value = data["lastName"];
        document.getElementById("email").value = data["email"];
        document.getElementById("phoneNumber").value = data["phoneNumber"];
        document.getElementById("address").value = data["address"];
        document.getElementById("city").value = data["city"];
        document.getElementById("state").value = data["state"];
        document.getElementById("zipCode").value = data["zipCode"];
        document.getElementById("password").value = data["password"];
        document.getElementById("fiatWalletID").value = data["fiatWalletID"];
        document.getElementById("fiatWalletID").readOnly = true;
        document.getElementById("dogecoinWalletID").value = data["dogecoinWalletID"];
        document.getElementById("dogecoinWalletID").readOnly = true;
        document.getElementById("title").innerText = "Update User Account Record";
        break;
    case 3:
        document.getElementById("fiatWalletID").value = data["fiatWalletID"];
        document.getElementById("fiatWalletID").readOnly = true;
        document.getElementById("fiatWalletName").value = data["fiatWalletName"];
        document.getElementById("fiatWalletBalance").value = data["fiatBalance"];
        document.getElementById("title").innerText = "Update Fiat Wallet Record";
        break;
    case 4:
        document.getElementById("dogecoinWalletID").value = data["dogecoinWalletID"];
        document.getElementById("dogecoinWalletID").readOnly = true;
        document.getElementById("walletAddress").value = data["walletAddress"];
        document.getElementById("walletAddress").readOnly = true;
        document.getElementById("dogecoinBalance").value = data["dogecoinBalance"];
        document.getElementById("title").innerText = "Update Dogecoin Wallet Record";
        break;
}