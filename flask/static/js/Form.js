var identifier = {0: "exchangeID",1: "txID",2: "userID",3: "fiatWalletID",4:"dogecoinWalletID"};


var data = JSON.parse(document.getElementById("query").innerHTML);

for (var i = 0; i<5; i++){
    if(identifier[i] in data){
        var value = i;
        break;
    }
}

switch(value){
    case 0:
        console.log("exchangeID");
        break;
    case 1:
        console.log("txID");
        break;
    case 2:
        console.log("userID");
        break;
    case 3:
        document.getElementById("fiatWalletId").value = data["fiatWalletID"];
        document.getElementById("fiatWalletId").readOnly = true;
        document.getElementById("fiatWalletName").value = data["fiatWalletName"];
        document.getElementById("fiatWalletBalance").value = data["fiatBalance"];
        break;
    case 4:
        console.log("dogecoinWalletID");
        break;
}



