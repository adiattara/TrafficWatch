
import org.apache.spark.sql.{SparkSession,DataFrame}
import org.apache.spark.sql.functions._
import org.apache.spark.sql.streaming.Trigger
import Transformation._
import Connectors._
object RoadTraffic extends App {

  // Load the configuration file

  val inputStream = ConfigManager.getStreamInput
  val checkpointPath = ConfigManager.getCheckpointPath

  val cloudCheckpointPath = ConfigManager.getCloudCheckpointPath
  val cloudSinkPath = ConfigManager.getCloudSinkPath
  val cloudInputStream = ConfigManager.getCloudInputStream


  val spark = SparkSession.builder
    .master("local[*]")
    .appName("Streaming Process Files")
    .config("spark.hadoop.fs.s3a.access.key", ConfigManager.getAccesKey) // Set the AWS access key
    .config("spark.hadoop.fs.s3a.secret.key", ConfigManager.getAccesKey)  // Set the AWS secret key
    .config ("spark.hadoop.fs.s3a.endpoint.region", "eu-west-1")   // Set the AWS region
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .getOrCreate()


  spark.conf.set("spark.sql.streaming.schemaInference", "true")
  val modeUDF = udf(mode)

  // Create the json to read from the input directory
  val jsonDF = spark.readStream
    .format("json")
    .option("maxFilesPerTrigger", 1)
    .load(inputStream)

  val StreamDF = jsonDF
    .withColumn("result", explode(col("results")))
    .select(
      col("result.datetime").as("datetime"),
      col("result.predefinedlocationreference").as("predefinedlocationreference"),
      col("result.averagevehiclespeed").as("averagevehiclespeed"),
      col("result.traveltime").as("traveltime"),
      col("result.traveltimereliability").as("traveltimereliability"),
      col("result.trafficstatus").as("trafficstatus"),
      col("result.vehicleprobemeasurement").as("vehicleprobemeasurement"),
      col("result.geo_point_2d").as("Geo Point"),
      col("result.geo_shape.type").as("Geo Shape"),
      col("result.hierarchie").as("hierarchie"),
      col("result.hierarchie_dv").as("hierarchie_dv"),
      col("result.denomination").as("denomination"),
      col("result.insee").as("insee"),
      col("result.sens_circule").as("sens_circule"),
      col("result.vitesse_maxi").as("vitesse_maxi")
    )

  val streamDfBis = StreamDF.withColumn("datetime", to_timestamp(col("datetime")).as("datetime"))

  val aggDF = myAggregation(streamDfBis)

  aggDF
    .writeStream
    .option("checkpointLocation", checkpointPath)
    .outputMode("append").foreachBatch(save_to_database(_, _))
    .trigger(Trigger.ProcessingTime("60 seconds"))
    .start()
    .awaitTermination()
}