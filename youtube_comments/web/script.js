const commentInput = document.getElementById("comment-input");
const submitComment = document.getElementById("submit-comment");
const resultDiv = document.getElementById("result");

submitComment.addEventListener("click", () => {
    let comment = commentInput.value;
    if (comment !== "") {
        eel.save_comment(comment)(displayResult);
    }
});

function displayResult(sentiment) {
    resultDiv.innerHTML = `
        <p>TextBlob Sentiment: ${sentiment.textblob}</p>
        <p>VADER Sentiment: ${sentiment.vader}</p>
        <p>Custom Sentiment: ${sentiment.custom}</p>
        <p>Best Algorithm: ${sentiment.best_algorithm}</p>
        <p>Best Sentiment: <strong>${sentiment.best_sentiment}</strong></p>
    `;
    commentInput.value = "";
}
