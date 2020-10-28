export default function ({ $axios }) {
  // $axios.onError(error => {
  //   if(error.response.status === 500) {
  //     redirect('/sorry')
  //   }
  // })
  $axios.setHeader('Authorization', '456')
}
