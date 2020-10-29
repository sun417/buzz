// try{
// 	var mysql      = require('mysql');
// var connection = mysql.createConnection({
// 	  host     : 'localhost',
// 	  user     : 'root',
// 	  password : '123123',
// 	  database : 'yzmcms'
// });

// connection.connect();

// //let sql = 'Select Count(1) From yzm_article Where title=?'
// let sql = 'Select * From yzm_article Limit 3'
// let params = ['2024年第35届国际病理学会双年会（IAP)']
// connection.query(sql, params, function (error, results, fields) {
// 	  if (error) throw error;
// 	  console.log('The solution is: ', results);
// });

// connection.end();
// } catch(err){
// 	console.log(err);
// }
class MyClass {
	static myStaticProp = 42;
  
	constructor() {
	  console.log(MyClass.myStaticProp); // 42
	}
  }