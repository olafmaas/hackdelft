$(document).ready(function () {
    loadTopics()
});

function loadTopics()
{
    $.ajax({
        url: "api/articles/1",
        success: function (payload){processTopics(payload)},
    });
}


function processTopics(topics) {
    topics.forEach(function(topic, index){ generate_view(topic, index)})
}

function generate_view(topic, index) {
    console.log(topic);
    $("#topiclist").append('<div class="topic row" id="'+index+'">'+topic.topics.map(function (x) {
            return x[0]
        }).join(" ")+'</div>')


    $("#"+index).click(function () {
        loadUrls(topic.articles)
    })
}

function loadUrls(articles) {
    $("#articlelist").empty()
    articles.forEach(function(article){
        $("#articlelist").append('<div class="row article">🔗 <a href="'+article.url+'">'+article.title+'</a></div>')
    })

}