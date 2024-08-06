import com.typesafe.config.ConfigFactory
import org.apache.spark.sql.functions.lit
import org.apache.spark.sql.{DataFrame, Dataset, Row}

object Connectors {

  private val config = ConfigFactory.load("application.conf")
  val user = config.getString("POSTGRES.user")
  val password = config.getString("POSTGRES.password")
  val database= config.getString("POSTGRES.database")
  val host = config.getString("POSTGRES.host")
  val port = config.getString("POSTGRES.port")
  val url = s"jdbc:postgresql://$host:$port/$database"

  def save_to_database(df: DataFrame, epoch_id: Long,table:String): Unit = {
    // Écrire batchDFWithBatchId dans la base de données


    df.write
      .format("jdbc")
      .mode("append")
      .option("url", url)
      .option("driver", "org.postgresql.Driver")
      .option("dbtable", table)
      .option("user", user)
      .option("password", password)
      .save()
  }

  def saveToCSV(df: Dataset[Row], batchId: Long, outputDir: String): Unit = {
    val batchOutputDir = s"$outputDir/batch_$batchId"
    df
      .write
      .option("header", "true")
      .csv(batchOutputDir)
  }

}
