/*
Javascript for Deep Community.
*/

community = {};

// This requires js-cookie
community.addKeyword = function() {
    var w = $("#new-keyword").val()
    if (w.includes(",")) {
        alert("Keyword can not include comma.");
        return;
    }
    if (w.length > 80) {
        alert("Keyword can not longer than 80 chars.")
        return;
    }
    $("#new-keyword").val("")
    var keywords = Cookies.get('keywords');
    if (!keywords) {
        var kwList = [];
    } else {
        var kwList = keywords.split(",");
    }
    if (kwList.length > 10) {
        alert("No more than 10 keywords, please.");
        return;
    }
    kwList.push(w.trim());
    var newKeywords = kwList.join(",");
    Cookies.set("keywords", newKeywords);
    community.showKeywords();
};

community.removeKeyword = function(e) {
    var w = $(e).html()
    var keywords = Cookies.get('keywords');
    if (!keywords) {
        var kwList = [];
    } else {
        var kwList = keywords.split(",");
    }
    var index = kwList.indexOf(w);
    if (index > -1) {
        kwList.splice(index, 1);
    }
    var newKeywords = kwList.join(",");
    Cookies.set("keywords", newKeywords);
    community.showKeywords();
};

community.showKeywords = function() {
    var newHtml = "";
    var keywords = Cookies.get('keywords');
    if (!keywords) {
        var kwList = [];
    } else {
        var kwList = keywords.split(",");
    }
    kwList.forEach(function(kw){
        newHtml += '<span class="label label-success" onclick="community.removeKeyword(this);">' + kw + '</span>';
    });
    $("#keywords").html(newHtml);
};

community.init = function() {
    community.showKeywords();
    $("#new-keyword-btn").click(community.addKeyword);
    $('#new-keyword').keypress(function (e) {
     var key = e.which;
     if(key == 13)  // the enter key code
      {
        $('#new-keyword-btn').click();
        return false;
      }
    });
};
