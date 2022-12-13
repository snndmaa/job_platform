let picup = document.getElementById('picup')


picup.addEventListener('change', () => {
    let form = document.getElementsByClassName('picForm')[0]
    form.submit()
})

const deleteJobPost = (id) => {
    let answer = window.confirm("Are you sure you want to delete this post?")
    if(answer){
        fetch('http://localhost:8000/dashboard', {
        method: 'DELETE',
        body: JSON.stringify({'id': id}),
        })
        .catch(e=>console.log(e))
        location.reload()
    }
    else{
        ''
    }

}