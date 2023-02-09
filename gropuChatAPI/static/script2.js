const accessToken = '3796899bd37c423bad3a21a25277bce0'
const baseUrl = 'http://127.0.0.1:8000/apichat/'
const sessionId = '20150910';
const loader = `<span class='loader'><span class='loader__dot'></span><span class='loader__dot'></span><span class='loader__dot'></span></span>`
const errorMessage = 'My apologies, I\'m not avail at the moment, however, please Visit Again.'
const urlPattern = /(\b(https?|ftp):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gim
const $document = document
const $chatbot = $document.querySelector('.chatbot')
const $chatbotMessageWindow = $document.querySelector('.chatbot__message-window')
const $chatbotHeader = $document.querySelector('.chatbot__header')
const $chatbotMessages = $document.querySelector('.chatbot__messages')
const $chatbotInput = $document.querySelector('.chatbot__input')
const $chatbotSubmit = $document.querySelector('.chatbot__submit')

const botLoadingDelay = 1000
const botReplyDelay = 2000

document.addEventListener('keypress', event => {
  if (event.which == 13) validateMessage()
}, false)

$chatbotHeader.addEventListener('click', () => {
  toggle($chatbot, 'chatbot--closed')
  $chatbotInput.focus()
}, false)

$chatbotSubmit.addEventListener('click', () => {
  validateMessage()
}, false)

const toggle = (element, klass) => {
  const classes = element.className.match(/\S+/g) || [],
    index = classes.indexOf(klass)
  index >= 0 ? classes.splice(index, 1) : classes.push(klass)
  element.className = classes.join(' ')
}

const userMessage = content => {
  $chatbotMessages.innerHTML += `<li class='is-user animation'>
      <p class='chatbot__message'>
        ${content}
      </p>
      <span class='chatbot__arrow chatbot__arrow--right'></span>
    </li>`
}

const aiMessage = (content, isLoading = false, delay = 0) => {
  setTimeout(() => {
    removeLoader()
    $chatbotMessages.innerHTML += `<li 
      class='is-ai animation' 
      id='${isLoading ? "is-loading" : ""}'>
        <div class="is-ai__profile-picture">
          <svg class="icon-avatar" viewBox="0 0 32 32">
            <use xlink:href="#avatar" />
          </svg>
        </div>
        <span class='chatbot__arrow chatbot__arrow--left'></span>
        <div class='chatbot__message'>${content}</div>
      </li>`
    scrollDown()
  }, delay)
}

const removeLoader = () => {
  let loadingElem = document.getElementById('is-loading')
  if (loadingElem) $chatbotMessages.removeChild(loadingElem)
}

const escapeScript = unsafe => {
  const safeString = unsafe
    .replace(/</g, ' ')
    .replace(/>/g, ' ')
    .replace(/&/g, ' ')
    .replace(/"/g, ' ')
    .replace(/\\/, ' ')
    .replace(/\s+/g, ' ')
  return safeString.trim()
}

const linkify = inputText => {
  return inputText.replace(urlPattern, `<a href='$1' target='_blank'>$1</a>`)
}

const validateMessage = () => {
  const text = $chatbotInput.value
  const safeText = text ? text : ''
  if (safeText.length && safeText !== ' ') {
    resetInputField()
    userMessage(safeText)
    sendForStore(safeText)
  }
  scrollDown()
  return
}

const processResponse = val => {
  let output = val
  removeLoader()
  return output
}

const setResponse = (val, delay = 0) => {
  setTimeout(() => {
    aiMessage(processResponse(val))
  }, delay)
}


const resetInputField = () => {
}


const scrollDown = () => {
  const distanceToScroll =
    $chatbotMessageWindow.scrollHeight -
    ($chatbotMessages.lastChild.offsetHeight + 60)
  $chatbotMessageWindow.scrollTop = distanceToScroll
  return false
}



// Function to GET csrftoken from Cookie
const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

let user

function loggedInUser(usrId, usrName, roomInUse) {
  user = { 'usrId': usrId, 'usrName': usrName, 'room':roomInUse }
  console.log(user, "Logged In User");
  return user;
}


function sendForStore(input) {


  var prompt = $chatbotInput.value;
  console.log("This is logged in user", user);
  $chatbotInput.value = '';

  // console.log(user, "This is user")
  // $.post('http://127.0.0.1:8000/api/messages/update/db',
  //   '{"user_input": ' + input + '"user": ' + user + '}',
  //   function (data) {
  //     console.log(data);
  //   })
  $.ajax({
      url: `http://127.0.0.1:8000/api/messages/update/db`,
      type: "POST",
      dataType: "json",
      data: {prompt: prompt,user: user},
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrfToken, 
      },
      success: (data) => {
      setResponse(data.response, botLoadingDelay + botReplyDelay)
      },
      error: (error) => {
        setResponse(errorMessage, botLoadingDelay + botReplyDelay)
        resetInputField()
        console.log(error)
      },
  })   


}

const send = (text = '') => {

  var prompt = $chatbotInput.value;
  console.log("This is logged in user", user);
  $chatbotInput.value = '';

  console.log(user, "This is user")
  $.ajax({
    url: `${baseUrl}`,
    type: "POST",
    dataType: "json",
    data: { prompt: prompt, user: user },
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": csrfToken,
    },
    success: (data) => {
      setResponse(data.response, botLoadingDelay + botReplyDelay)
    },
    error: (error) => {
      setResponse(errorMessage, botLoadingDelay + botReplyDelay)
      resetInputField()
      console.log(error)
    },
  })

  aiMessage(loader, true, botLoadingDelay)
}




// const send = (text = '') => {
//     // Get the form data
//     var prompt = $chatbotInput.value;
//     $chatbotInput.value = '';



// fetch(`${baseUrl}`, {
//     method: 'POST',
//     // dataType: 'json',
//     body:JSON.stringify({prompt: prompt + "====================" }),
//     //     prompt:name,
//     //     body:body,

//     //   }),

//     // credentials: "same-origin",
//     headers: {
//       "Accept": "application/json",
//       'Content-Type': 'application/json',
//       'X-CSRFToken': csrfToken
//     },
//   })
//   .then(response => response.json())
//   .then(res => {
//     if (res.status < 200 || res.status >= 300) {
//       let error = new Error(res.statusText)
//       throw error
//     }
//     return res
//   })
//   .then(res => {
//     console.log('this is a response',res)
//     setResponse(res.response, botLoadingDelay + botReplyDelay)
//   })
//   .catch(error => {
//     setResponse(errorMessage, botLoadingDelay + botReplyDelay)
//     resetInputField()
//     console.log(error)
//   })

//   aiMessage(loader, true, botLoadingDelay)
// }


function receive() {
  $.get('/api/messages/' + sender_id + '/' + receiver_id, function (data) {
    alert(data);
    if (data.length !== 0) {
      for (var i = 0; i < data.length; i++) {
        var box = text_box.replace('{sender}', data[i].sender);
        box = box.replace('{message}', data[i].message);
        box = box.replace('right', 'left blue lighten-5');
        $('#board').append(box);
        scrolltoend();
      }
    }
  })
}