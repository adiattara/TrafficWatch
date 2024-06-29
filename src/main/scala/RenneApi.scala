import com.typesafe.config.ConfigFactory
import org.apache.hadoop.fs.{FileSystem, Path}
import org.apache.spark.sql.SparkSession
import scalaj.http.Http

import java.io.PrintWriter
import java.nio.file.{Files, Paths}
import scala.concurrent.duration._
object RenneApi extends App {

  val apiUrl = ConfigManager.getApiUrl
  val apiOutput = ConfigManager.getApiOutput
  val inputStream = ConfigManager.getInputStream
  val cloudInputStream = ConfigManager.getCloudInputStream
  val accesKey = ConfigManager.getAccesKey
  val awsSecret = ConfigManager.getAwsSecret

  val spark = SparkSession.builder
    .master("local[*]")
    .appName("Fetch Api Files")
    .config("spark.hadoop.fs.s3a.access.key", accesKey) // Set the AWS access key
    .config("spark.hadoop.fs.s3a.secret.key", awsSecret)  // Set the AWS secret key
    .config ("spark.hadoop.fs.s3a.endpoint.region", "eu-west-1")   // Set the AWS region
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .getOrCreate()

  def fetchDataAndWriteToS3(): Unit = {
      // fetch data from the api
      val response = Http(apiUrl).asString

      // convert data to json
      val jsonString = response.body

      // create a file name based on the current timestamp
      val fileName = s"${System.currentTimeMillis()}.json"

      // write the json response to  s3 bucket
      val filePath = new Path(s"$cloudInputStream/$fileName")

      // get the Hadoop FileSystem
      val fs = FileSystem.get(new java.net.URI(s"s3a://trafficwatch1"), spark.sparkContext.hadoopConfiguration)

      // create an output stream
      val outputStream = fs.create(filePath)

      // write the data
      outputStream.writeBytes(jsonString)

      // close the stream
      outputStream.close()

      //todo : use logger instead of println
      println(s"Data written to file: $fileName in S3 bucket: $cloudInputStream")
  }
  def fetchDataAndWriteToFile(): Unit = {
    val response = Http(apiUrl).asString

    // convert data to json
    val jsonString = response.body

    // create a file name based on the current timestamp
    val fileName = s"${System.currentTimeMillis()}.json"
    val filePath = Paths.get(apiOutput, fileName)

    // write data to file
    Files.createDirectories(filePath.getParent)
    val writer = new PrintWriter(filePath.toFile)
    writer.write(jsonString)
    writer.close()

     //todo: use logger instead of println
    println(s"Data written to file: $fileName")
  }
  //define a scheduler to fetch data every minute
  val duration = Duration(1, MINUTES)
  val scheduler = new java.util.Timer()

  scheduler.schedule(new java.util.TimerTask {
    def run() = {
      fetchDataAndWriteToFile()
    }
  }, 0, duration.toMillis)

  // Keep the application running indefinitely
  while (true) {
    Thread.sleep(1000)
  }


}
