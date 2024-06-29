import org.apache.spark.sql.{DataFrame, Dataset, Row}

object Connectors {



  def save_to_database(df: DataFrame, epoch_id: Long): Unit = {
    df.write
      .format("jdbc")
      .mode("append")
      .option("url", "jdbc:postgresql://localhost:5432/spark_db")
      .option("driver", "org.postgresql.Driver")
      .option("dbtable", "traffic")
      .option("user", "spark_user")
      .option("password", "password")
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
