// JavaScript source code
var page_num = 10
var offset = 0
var attraction_list = []
var is_attraction_empty = false
var is_experience_empty = false
var experience_list = []
var current_type = 0 //0: attraction, 1: experience
var global_search_txt = ""
function search_click() {
    search_txt = $("#search_box").val()
    if (search_txt == "") {
        back_2_index()
    }
    else {
        window.location.href = "search.html?keyword=" + search_txt + "&type=" + current_type;
    }
}

function back_2_index() {
    window.location.href="../index.html"
}

function switch_search_page_type() {
    $("#main_div").html("")
    if (current_type == 0) {
        idx = 0;
        document.getElementById('experience').className = "unselected";
        document.getElementById('attraction').className = "selected";
        while (idx < attraction_list.length) {
            $("#main_div").append("<div class=\"block\"><h3>city: " + attraction_list[idx][0] + "</h3>\
           <p> score: "+ attraction_list[idx][1] + "<\p>\
            <p>attraction: " + attraction_list[idx][2] +"<\p>\
        </div>");
            idx = idx + 1;
        }
    }
    else if (current_type == 1) {
        idx = 0;
        document.getElementById('experience').className = "selected";
        document.getElementById('attraction').className = "unselected";
        while (idx < attraction_list.length) {
            $("#main_div").append("<div class=\"block\"><h3>city: " + experience_list[idx][0] + "</h3>\
            <p>experience: " + experience_list[idx][1] +"<\p>\
        </div>");
            idx = idx + 1;
        }
    }
}

function add_attraction_data(data) {
    if (is_attraction_empty) {
        return;
    }
    if (data.length == 0) {
        is_attraction_empty = true;
        $("#main_div").append("<div class=\"block\"><p style=\"font-style: italic\">已抵达查询末尾...<p></div>")
        return;
    }
    idx = 0
    while (idx < data.length) {
        
        $("#main_div").append("<div class=\"block\"><h3>city: " + data[idx][0] + "</h3>\
           <p> score: "+ data[idx][1] +"<\p>\
            <p>attraction: " + data[idx][2] +"<\p>\
        </div>");
        idx = idx + 1;
    }
    
}
function add_experience_data(data) {
    if (data.length == 0) {
        is_experience_empty = true;
        $("#main_div").append("<div class=\"block\"><p style=\"font-style: italic\">已抵达查询末尾...<p></div>")
        return;
    }
    idx = 0
    while (idx < data.length) {
        $("#main_div").append("<div class=\"block\"><h3>city: " + data[idx][0] + "</h3>\
            <p>experience: " + data[idx][1] +"<\p>\
        </div>");
        idx = idx + 1;
    }
}

function get_info_fromDB(search_txt) {
    if (is_attraction_empty && current_type == 0) {
        return;
    }
    if (is_experience_empty && current_type == 1) {
        return;
    }
    $.get("http://127.0.0.1:8001/search",
        {
            "search_data": search_txt,
            "page_num": page_num,
            "offset": offset
        },
        function (data) {
            var i = 0;
            while (i < data["attraction"].length) {
                attraction_list.push(data["attraction"][i])
                i = i + 1;
            }
            i = 0
            while (i < data["experience"].length) {
                experience_list.push(data["experience"][i])
                i = i + 1;
            }
            if (current_type == 0) {
                add_attraction_data(data["attraction"]);
            }
            else if (current_type == 1) {
                add_experience_data(data["experience"])
            }

        },
        "json")
    offset = offset + page_num
}

$(document).ready(function () {
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    global_search_txt = ""
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split("=");
        if (pair[0] == "keyword") {
            $("#search_box").val(decodeURIComponent(pair[1])); 
            global_search_txt = decodeURIComponent(pair[1])
        }
        if (pair[0] == "type") {
            current_type = pair[1]
            switch_search_page_type()
        }
    }
    if (global_search_txt == "") {
        back_2_index()
    }
    get_info_fromDB(global_search_txt)
    
    $(window).scroll(function () {
        if ($(document).scrollTop() >= $(document).height() - $(window).height()) {
            get_info_fromDB(global_search_txt)
        }
    });
})

//$(document).ready(function () {
//    console.log("启动！");
//    var senddata = {
//        "search_data": "pa p"
//        ,
//        "page_num": 10,
//        "offset": 0
//    }

//    console.log(senddata)
//    $.get("http://127.0.0.1:8001/search",
//        senddata,
//        function (data) {
//            var i = 0;
//            console.log(data);
//            { attraction: Array(10), experience: Array(10) }
//            attraction: Array(10)
//            // data shape: {attraction: Array(10), experience: Array(10)}

//            // attraction: Array(10)
//            //0: "Eiffel Tower"
//            //1: "Centre Pompidou"
//            //2: "Sainte-Chapelle"
//            //3: "Musée du Louvre"
//            //4: "Les Catacombes"
//            //5: "Musée Rodin"
//            //6: "Jardin du Luxembourg"
//            //7: "Panthéon"
//            //8: "Musée d’Orsay"
//            //9: "Jardin des Tuileries"
//            //length: 10
//            //[[Prototype]]: Array(0)

//            //experience: Array(10)
//            //0: "Skip the Line - Closing Time with the Mona Lisa"
//            //1: "Experience Bohemian Paris"
//            //2: "Three Hour Marais Tour "
//            //3: "Eiffel Tower Priority Access Guided Tour with Summit Access"
//            //4: "Paris Sightseeing Family Friendly Guided Electric Bike Tour"
//            //5: "Louvre & Orsay Museums Skip-the-line Semi-Private Guided Combo Tour"
//            //6: "Skip the Line: Eiffel Tower Tickets and Small-Group Tour"
//            //7: "Private Guided Photoshoot Experience at the Eiffel Tower"
//            //8: "Louvre Museum Skip-the-Line Guided Tour with Venus de Milo & Mona Lisa"
//            //9: "Eiffel Tower Dinner Experience & Sightseeing Seine River Cruise"
//            //length: 10
//            //[[Prototype]]: Array(0)
//            //[[Prototype]]: Object
//        },
//        "json")
//    console.log("结束！");
//}
//);


function choose_search_type(btn) {
    btn.className = "selected";
    if (btn.id == "attraction") {
        current_type = 0 // 0->attraction
        document.getElementById('experience').className = "unselected";
        switch_search_page_type();
    }
    else {
        current_type = 1 // 1->experience
        document.getElementById('attraction').className = "unselected";
        switch_search_page_type();
    }
}