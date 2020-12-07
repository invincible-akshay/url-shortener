import java.util.List;
import java.util.ArrayList;
import java.util.Iterator;
/* Spark imports */
import scala.Tuple2;

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.api.java.function.Function2;
import org.apache.spark.api.java.function.PairFlatMapFunction;

public class SparkUrlCount {

    
    /**
     * args[0]: Input file path on distributed file system
     * args[1]: Output file path on distributed file system
     */
    public static void main(String[] args) throws Exception{
	
    	// the output directory to store the results, this needs to be deleted every time we run this.
	    String output = args[1];
		
	    /* essential to run any spark code */
		SparkConf conf = new SparkConf().setAppName("SparkUrlCount").setMaster("local");
		JavaSparkContext sc = new JavaSparkContext(conf);
	
		/* load input data to RDD */
		/* our big url counts file to map reduce */ 
		JavaRDD<String> dataRDD = sc.textFile(args[0]);
	
		JavaPairRDD<String, Integer> counts =
		    dataRDD.flatMapToPair(new PairFlatMapFunction<String, String, Integer>(){
				private static final long serialVersionUID = 1L;
	
				public Iterator<Tuple2<String, Integer>> call(String value){
			    	List<Tuple2<String, Integer>> retWords = new ArrayList<Tuple2<String, Integer>>();
			    	String[] values = value.toString().split(",");
			    	if(values.length <2) {
			    		return retWords.iterator();
			    	}
			    	try {
			    		retWords.add(new Tuple2<String, Integer>(values[0], Integer.parseInt(values[values.length-1])));
			    	} catch(NumberFormatException ex) {
			    		
			    	}
					return retWords.iterator();
			    }
			}).reduceByKey(new Function2<Integer, Integer, Integer>(){
				private static final long serialVersionUID = 1L;
	
				public Integer call(Integer x, Integer y){
				    return x+y;
				}
			    });
		counts.saveAsTextFile(output);
	    sc.close();
    }
}
