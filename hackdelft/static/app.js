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

    var topic_words = topic.topics.map(function (x) {
            return x[0]
        });
    console.log("test");
    $("#topiclist").append('<div class="topic row" id="'+index+'"><div class="left">'+topic.goodactivity+'</div><div class="right">'+topic_words.join(", ")+'</div></div>')



    $("#"+index).click(function () {
        loadUrls(topic.articles, topic_words)
    })
}

function loadUrls(articles, topics) {
    $("#articlelist").empty()
    articles.sort(function(a1, a2){
        // console.log(topics)
        // console.log(a2.title.toLowerCase().split(" "))

        return _.intersection(a2.title.toLowerCase().split(" "), topics).length -
        _.intersection(a1.title.toLowerCase().split(" "), topics).length
    }).forEach(function(article){
        $("#articlelist").append('<div class="row article">🔗 <a href="'+article.url+'">'+article.title+'</a></div>')
    })

}