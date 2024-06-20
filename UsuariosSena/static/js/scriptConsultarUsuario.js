function filtrarTabla() {
    const input = document.getElementById('filtroEdad');
    const filter = input.value.toUpperCase();
    const table = document.getElementById('tablaPersonas');
    const rows = table.getElementsByTagName('tr');
  
    for (let i = 1; i < rows.length; i++) {
      let shouldShow = false;
  
      const cells = rows[i].getElementsByTagName('td');
      for (let j = 0; j < cells.length - 1; j++) {
        const cellText = cells[j].innerText || cells[j].textContent;
        if (cellText.toUpperCase().includes(filter)) {
          shouldShow = true;
          break;
        }
      }
  
      if (shouldShow || filter === '') {
        rows[i].style.display = '';
      } else {
        rows[i].style.display = 'none';
      }
    }
  }
