'use strict';
document.querySelectorAll('form[data-confirm]').forEach(form => {
  const submit = form.querySelector('button[type="submit"], button:not([type])');
  if (!submit) return;
  const originalLabel = submit.textContent;
  let pending = false;
  let notice;
  let cancel;
  const reset = () => {
    pending = false;
    notice?.remove();
    cancel?.remove();
    submit.textContent = originalLabel;
    submit.focus();
  };
  form.addEventListener('submit', event => {
    if (pending) return;
    event.preventDefault();
    pending = true;
    notice = document.createElement('p');
    notice.textContent = form.dataset.confirm;
    notice.setAttribute('role', 'status');
    cancel = document.createElement('button');
    cancel.type = 'button';
    cancel.textContent = 'Cancelar';
    cancel.addEventListener('click', reset);
    submit.textContent = 'Confirmar devolução';
    form.prepend(notice);
    form.append(cancel);
    cancel.focus();
  });
  form.addEventListener('keydown', event => {
    if (pending && event.key === 'Escape') {
      event.preventDefault();
      reset();
    }
  });
});
