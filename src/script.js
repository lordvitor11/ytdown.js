import { makeConfig, addSong, getSong, getLen, removeSong_, downloadSong_, getPath_, quit } from './renderer.js';

let hasAdd = false;

let progress = 0;

export async function increaseProgress() {
  const respostaLen = await getJsonLen();
  if (progress < 100) {
    progress += 100 / respostaLen['num'];
    document.getElementById('loader-2').style.width = progress + '%';
  }
}

export function getPath() {
  return new Promise((resolve, reject) => {
    getPath_()
    .then(resposta => { resolve(resposta.dir); })
    .catch(error => { reject(error); })
  });
}

function getString() {
  let string = document.querySelector('#caminho').textContent;
  string = string.replace("Caminho selecionado: ", "");
  return string;
}

export async function changeText() {
  const caminhoPasta = await getPath();
  const caminhoSelecionadoSpan = document.getElementById('caminho');
  let nextButton = document.getElementById('next');

  caminhoSelecionadoSpan.textContent = `Caminho selecionado: ${caminhoPasta}`;
  nextButton.disabled = false;
  nextButton.classList.remove('disabled');
}

function showNotification(texto) {
  let notificationElement = document.querySelector('.notification');
  notificationElement.textContent = texto;
  notificationElement.style.opacity = "1";

  setTimeout(() => {
    notificationElement.style.opacity = "0";
  }, 3000);
}

export function config() {
  makeConfig(getString())
  .then(resposta => { window.location.href = "index.html"; })
  .catch(error => { console.log(error); });
}

export function adc() {
  let input = document.getElementById('link');

  if (input.value != '') {
    addSong(input.value).then(resposta => {
      if (resposta['resposta'] == 0) {
        showNotification("Música adicionada com sucesso!");
      } else {
        showNotification("Música já adicionada!");
      }  
    }).catch(error => { console.log(error); });

    input.value = "";
    hasAdd = true;
    document.querySelector("#download").disabled = false;
    document.querySelector("#download").classList.remove('disabled');
  } else {
    showNotification("Deve adicionar um link!");
  }
}

export function baixar() {
  if (hasAdd) {
    window.location.href = "check.html";
  } else {
    showNotification(texto = "Deve adicionar uma música!");
  }
}

export function getJsonLen() {
  return new Promise((resolve, reject) => {
    getLen().then(resultado => {
      if (resultado.resposta == 0) { resolve({ num: resultado.numero, links: resultado.links }); } else { reject("Erro"); }
    })
  })
}

function addListener() {
  const checks = document.querySelectorAll('.check');
  let active = false;

  for (let c = 0; c < checks.length; c++) {
      if (checks[c].checked) {
          active = true;
      }
  }

  if (active) {
      document.querySelector('#remover').disabled = false;
      document.querySelector('#remover').classList.remove('disabled');
  } else {
      document.querySelector('#remover').disabled = true;
      
      if (!document.querySelector('#remover').classList.contains('disabled')) { document.querySelector('#remover').classList.add('disabled'); }
  }
}

export async function getSongInfo() {
  let tableDiv = document.querySelector('.table');
  let table = document.createElement('table');
  let thead = document.createElement('thead');
  let trHead = document.createElement('tr');
  let thInput = document.createElement('th');
  let thSong = document.createElement('th');
  let thDuration = document.createElement('th');
  let tbody = document.createElement('tbody');
  let h1 = document.querySelector('.center h1');
  let buttonCheck = document.querySelector('.buttons-check');

  thInput.textContent = " ";
  thSong.textContent = 'Música';
  thDuration.textContent = 'Duração';
  trHead.appendChild(thInput);
  trHead.appendChild(thSong);
  trHead.appendChild(thDuration);
  thead.appendChild(trHead);

  const respostaLen = await getJsonLen();

  for (let c = 0; c < respostaLen['num']; c++) {
    const res = await getSong(respostaLen['links'][c]);
    if (res['resposta'] == 0) { 
      let tr = document.createElement('tr');
      let tdSong = document.createElement('td');
      let tdDuration = document.createElement('td');
      let checkbox = document.createElement('input');
      
      checkbox.type = 'checkbox';
      checkbox.id = c;
      checkbox.classList.add('check');
      tdSong.textContent = res['title'];
      tdDuration.textContent = res['duration'];

      tr.appendChild(checkbox);
      tr.appendChild(tdSong);
      tr.appendChild(tdDuration);

      tbody.appendChild(tr);
    } else {
        console.log("Deu erro!");
    }
  }

  table.appendChild(thead);
  table.appendChild(tbody);
  tableDiv.appendChild(table);

  const checks = document.querySelectorAll('.check');

  for (let c = 0; c < checks.length; c++) {
    checks[c].addEventListener('click', addListener);
  }

  h1.classList.remove('hide');
  buttonCheck.classList.remove('hide');
}

export async function removeSong() {
  const checks = document.querySelectorAll('.check');
  let ids = {};

  for (let c = 0; c < checks.length; c++) {
      if (checks[c].checked) {
          ids[c] = checks[c].id;
      }
  }

  if (ids.length != 0) {
    const respostaRemoveSong = await removeSong_(ids);
    if (respostaRemoveSong['resposta'] == 0) {
      const respostaLen = await getJsonLen();
      if (respostaLen['num'] == 0) { window.location.href = "index.html"; } else { location.reload(); }
    } else {
      console.log(respostaRemoveSong['resposta']);
    }
  }
}

export async function downloadSong() {
  let button = document.createElement('input');
  button.type = 'button';
  button.value = 'Sair';
  button.addEventListener('click', sair);

  const response = await downloadSong_();

  if (response['resposta'] == 1) {
    console.log('Deu erro!');
    showNotification('Deu erro!');
  } else {
    console.log('Músicas baixadas!');
    showNotification('Músicas baixadas!');
    document.querySelector('#result').textContent = "Todas suas músicas foram baixadas!";
    document.querySelector('.center').appendChild(button);
  }
}

export function sair() {
  quit();
}