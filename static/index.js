const RANDOM_QUOTE_API_URL = "https://api.quotable.io/random?minLength=80&maxLength=200"
const displayQuoteElement = document.getElementById("displayQuote")
const quoteInputElement = document.getElementById("quoteInput")
const timerElement = document.getElementById("timer")
const reloadElement = document.getElementById("reload")
const resultElement = document.getElementById("resultData")
const wpmElement = document.getElementById("wpm")

let timerstarted = false
let typedCharacters = 0;
let correctCharacters = 0;
let wpm = 0;
let accuracy = 0;
let backspace = 0;

if (reloadElement){
  reloadElement.addEventListener('click', () => {
    stopTimer()
    timerstarted = false
    renderQuote()
    typedCharacters = 0;
    correctCharacters = 0;
    backspace = 0;
    wpmElement.innerHTML = '';
    quoteInputElement.disabled = false;
    quoteInputElement.focus()
  })
}

if (quoteInputElement){
  quoteInputElement.addEventListener('input', (event) => {
      const arrayQuote = displayQuoteElement.querySelectorAll('span')
      console.log(arrayQuote)
      const arrayValue = quoteInputElement.value.split('')
      console.log(arrayValue)
      let correct = true
      arrayQuote.forEach((charSpan, index) => {
        const character = arrayValue[index]
        if (character == null) {
          charSpan.classList.remove('correct')
          charSpan.classList.remove('incorrect')
          correct = false
        } else if (character === charSpan.innerText) {
          charSpan.classList.add('correct')
          charSpan.classList.remove('incorrect')
          console.log(correctCharacters);
        } else {
          charSpan.classList.remove('correct')
          charSpan.classList.add('incorrect')
          correct = false
        }
      })
      if (correct) {
        stopTimer()
        timerstarted = false
        // document.getElementById('testResult').submit()

        quoteInputElement.disabled = true;

        let cpm = (typedCharacters - backspace) / timerElement.innerHTML * 60;
        wpm = Math.floor(cpm/5);
        accuracy = Math.round((correctCharacters / (typedCharacters - backspace)) * 100);

        timerElement.innerHTML = '';
        wpmElement.innerHTML += 'Your WPM is ' + wpm + ' with an Accuracy of ' + accuracy + '%';


        // send data to server
        send()
      }

      let key = event.data; // const {key} = event; ES6+
      if (key === null) backspace += 1;

      console.log(backspace);
      console.log(typedCharacters);
      console.log(correctCharacters);

      let inputLength = arrayValue.length - 1;
      if (arrayQuote[inputLength].innerText == arrayValue[inputLength]) correctCharacters +=1

      typedCharacters += 1;
  })
}

function getQuote() {
    return fetch(RANDOM_QUOTE_API_URL)
    .then(response => response.json())
    .then(data => data.content)
}


async function renderQuote(){
    const quote = await getQuote()
    if (displayQuoteElement){
    displayQuoteElement.innerHTML = ''
    quote.split('').forEach(character => {
        const charSpan = document.createElement('span')
        charSpan.innerText = character
        displayQuoteElement.appendChild(charSpan)
    })
    quoteInputElement.value = null
  }
}

let startTime
let interval
function startTimer() {
  timerElement.innerText = 0
  startTime = new Date()
  interval =setInterval(() => {
    timerElement.innerText = getTimerTime()
  }, 1000)
}

function getTimerTime() {
  return Math.floor((new Date() - startTime) / 1000)
}

function stopTimer() {
  clearInterval(interval);
}


renderQuote()
if (quoteInputElement){
  quoteInputElement.addEventListener('keydown', () => {
    if (!timerstarted) {
      startTimer()
      timerstarted = true
      }
    })
}

function send() {
  let response = fetch('/update?wpm=' + wpm + '&acc=' + accuracy);
}