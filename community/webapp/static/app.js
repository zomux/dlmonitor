/*
Javascript for Deep Community.
*/

INIT_KEYWORDS = "hot papers,reinforce learning,adversarial training";

community = {
    ajaxCount: 0
};

community.getKeywords = function() {
    var keywords = Cookies.get('keywords');
    if (Cookies.get('keywords') == undefined) {
        keywords = INIT_KEYWORDS;
    }
    if (!keywords) {
        var kwList = [];
    } else {
        var kwList = keywords.split(",");
    }
    return kwList;
};

// This requires js-cookie
community.addKeyword = function() {
    var w = $("#new-keyword").val()
    if (w.length == 0) {
        return;
    }
    if (w.includes(",")) {
        alert("Keyword can not include comma.");
        return;
    }
    if (w.length > 80) {
        alert("Keyword can not longer than 80 chars.")
        return;
    }
    $("#new-keyword").val("")
    var kwList = community.getKeywords();
    if (kwList.length > 10) {
        alert("No more than 10 keywords, please.");
        return;
    }
    kwList.push(w.trim());
    var newKeywords = kwList.join(",");
    Cookies.set("keywords", newKeywords);
    // community.showKeywords();
    community.updateAll();
};

community.removeKeyword = function(e) {
    var w = $(e).data('keyword');
    if (w == undefined) {
        return;
    }
    var kwList = community.getKeywords();
    var index = kwList.indexOf(w);
    if (index > -1) {
        kwList.splice(index, 1);
    }
    var newKeywords = kwList.join(",");
    Cookies.set("keywords", newKeywords);
    community.showKeywords();
    community.updateAll();
};

// Deprecated
community.showKeywords = function() {
    var newHtml = "";
    var kwList = community.getKeywords();
    kwList.forEach(function(kw){
        newHtml += '<span class="label label-success" onclick="community.removeKeyword(this);">' + kw + '</span>';
    });
    $("#keywords").html(newHtml);
};

community.fetch = function(src_name, keyword, index, start=0) {
    console.log("fetch", src_name, keyword, index, start);
    $("#posts-" + index).html(
        "<div style='text-align:center;'>"+
        "<img src='https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/0.16.1/images/loader-large.gif'/>"+
        "</div>");
    community.ajaxCount ++;
    $.ajax({
       url: '/fetch',
       type: 'POST',
       data: {
          src: src_name,
          start: "" + start,
          keyword: keyword
       },
       error: function() {
           community.ajaxCount --;
           alert("Error when fetching data.");
       },
       success: function(data) {
          // console.log(data);
          community.ajaxCount --;
          $("#posts-" + index).html(data);
       }
    });
};

community.convertDateInfo = function(token) {
    var dateinfo = "Recent two weeks";
    switch (token) {
        case '1-week':
            dateinfo = "Recent one week";
            break;
        case '2-week':
            dateinfo = "Recent two weeks";
            break;
        case '1-month':
            dateinfo = "Recent one month";
            break;
    }
    return dateinfo;
};

community.showDate = function() {
    var datetoken = Cookies.get('datetoken');
    if (!datetoken) {
        datetoken = '2-week';
    }
    $("#date-info").html(community.convertDateInfo(datetoken));
};

community.filterDate = function(token) {
    Cookies.set('datetoken', token);
    community.updateAll();
};

community.placeColumns = function() {
    var kwList = community.getKeywords();
    var currentNum = $(".post-columns .column").length
    // Create columns
    if (kwList.length != currentNum) {
        var newHtml = "";
        var template = $("#column-template").html()
        for (var i = 0; i < kwList.length; ++i) {
            newHtml += template.replace("NUM", "" + i).replace("NUM", "" + i).replace("NUM", "" + i);
        }
        $("#post-columns").html(newHtml);
    }
    // Fill titles
    $(".post-columns .column").css("float", "left");
    for (var i = 0; i < kwList.length; ++i) {
        $("#column-title-" + i).html(kwList[i]);
        $("#close-btn-" + i).data("keyword", kwList[i])
    }
};

// Deprecated
community.fixFloat = function() {
    if (community.ajaxCount != 0) return;
    var threshold = $("#post-columns").position().left + 1200 / 2;
    $(".post-columns .column").each(function(i, e) {
        if ($(e).position().left > threshold) {
            $(e).css("float", "right");
        }
    });
};

community.updateAll = function() {
    community.showDate();
    community.placeColumns();
    var kwList = community.getKeywords();
    for (var i = 0; i < kwList.length; ++i) {
        community.fetch('arxiv', kwList[i], i, start=0);
    }
};

community.init = function() {
    community.updateAll();
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
