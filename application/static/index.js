function deleteNote(noteId){
    fetch('/delnote',{
        method: 'POST',
        body: JSON.stringify({noteId:noteId})
    }).then((_res) => {
        window.location.href = '/';
    });
}