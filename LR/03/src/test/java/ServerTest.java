import org.json.simple.parser.ParseException;
import org.junit.After;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;

import java.io.IOException;
import java.util.Arrays;
import java.util.Collection;

import static org.hamcrest.CoreMatchers.is;
import static org.junit.Assert.assertThat;

@RunWith(value = Parameterized.class)
public class ServerTest2 {
	private String Gison;
    private Server server;
    private String expectedSilka;
    private String expectedNomer;
    private String expectedMesType;
    private String expectedNomerLabi;

    // Inject via constructor
    // for {8, 2, 10}, numberA = 8, numberB = 2, expected = 10
    public ServerTest2(String Gison,String expectedMesType,String expectedNomerLabi,
     String  expectedNomer,String expectedSilka) throws ParseException, IOException {
       this.Gison=Gison;
        this.expectedMesType=expectedMesType;
        this.expectedNomerLabi=expectedNomerLabi;
        this.expectedNomer=expectedNomer;
        this.expectedSilka=expectedSilka;
        server=new Server();
        server.OsnovaDecoda(Gison);
    }

    // name attribute is optional, provide an unique name for test
    // multiple parameters, uses Collection<Object[]>
    @Parameters(name = "{index}: ({0},{1}) = {2}")
    public static Collection<Object[]> data() {
        return Arrays.asList(new Object[][]{
        	{"мывфываацу","3","messageType, variant, link, lab","1","Неверная JSON строка"},
        	{"{\"messageType\":\"2\",\"variant\":\"1\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Losiash.git\",\"lab\":\"3\"}","3","messageType","3","Неверное значение"},
        	{"{\"messageType\":\"0\",\"variant\":\"1\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Losiash.git\",\"lab\":\"3\"}","3","messageType","3","Неверное значение"},
        	{"{\"messageType\":\"\",\"variant\":\"1\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Losiash.git\",\"lab\":\"3\"}","3","messageType","2","Отстуствует ключ"},
        	{"{\"messageType\":\"fds\",\"variant\":\"1\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Losiash.git\",\"lab\":\"3\"}","3","messageType","4","Не тот тип данных"},
        	{"{\"messageType\":\"1\",\"variant\":\"1\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Losiash.git\",\"lab\":\"0\"}","3","lab","3","Неверное значение"},
        	{"{\"messageType\":\"1\",\"variant\":\"1\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Losiash.git\",\"lab\":\"5\"}","3","lab","3","Неверное значение"},
        	{"{\"messageType\":\"1\",\"variant\":\"1\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Losiash.git\",\"lab\":\"\"}","3","lab","2","Отстуствует ключ"},
        	{"{\"messageType\":\"1\",\"variant\":\"1\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Losiash.git\",\"lab\":\"fas\"}","3","lab","4","Не тот тип данных"},
        	{"{\"messageType\":\"1\",\"variant\":\"0\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Losiash.git\",\"lab\":\"3\"}","3","variant","3","Неверное значение"},
        	{"{\"messageType\":\"1\",\"variant\":\"16\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Losiash.git\",\"lab\":\"3\"}","3","variant","3","Неверное значение"},
        	{"{\"messageType\":\"1\",\"variant\":\"\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Losiash.git\",\"lab\":\"3\"}","3","variant","2","Отстуствует ключ"},
        	{"{\"messageType\":\"1\",\"variant\":\"fsa\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Losiash.git\",\"lab\":\"3\"}","3","variant","4","Не тот тип данных"},
        	{"{\"messageType\":\"1\",\"variant\":\"1\",\"link\":\"https:\\/\\/github25.com\\/vvtatyana\\/Losiash.git\",\"lab\":\"3\"}","3","link","3","Неверное значение"},
        	{"{\"messageType\":\"1\",\"variant\":\"1\",\"link\":\"\",\"lab\":\"3\"}","3","link","2","Отстуствует ключ"},
        	
        	{"{\"messageType\":\"1\",\"variant\":\"1\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Losiash.git\",\"lab\":\"3\"}","1","3","1","https://github.com/vvtatyana/Losiash.git"},
        	{"{\"messageType\":\"1\",\"variant\":\"2\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Krosh.git\",\"lab\":\"3\"}","1","3","2","https://github.com/vvtatyana/Krosh.git"},
        	{"{\"messageType\":\"1\",\"variant\":\"3\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Yozhik.git\",\"lab\":\"3\"}","1","3","3","https://github.com/vvtatyana/Yozhik.git"},
        	{"{\"messageType\":\"1\",\"variant\":\"4\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Barash.git\",\"lab\":\"3\"}","1","3","4","https://github.com/vvtatyana/Barash.git"},
        	{"{\"messageType\":\"1\",\"variant\":\"5\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Nusha.git\",\"lab\":\"3\"}","1","3","5","https://github.com/vvtatyana/Nusha.git"},
        	{"{\"messageType\":\"1\",\"variant\":\"6\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Pin.git\",\"lab\":\"3\"}","1","3","6","https://github.com/vvtatyana/Pin.git"},
        	{"{\"messageType\":\"1\",\"variant\":\"7\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Sovunya.git\",\"lab\":\"3\"}","1","3","7","https://github.com/vvtatyana/Sovunya.git"},
        	{"{\"messageType\":\"1\",\"variant\":\"8\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Pandi.git\",\"lab\":\"3\"}","1","3","8","https://github.com/vvtatyana/Pandi.git"},
        	{"{\"messageType\":\"1\",\"variant\":\"9\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Kar-Karych.git\",\"lab\":\"3\"}","1","3","9","https://github.com/vvtatyana/Kar-Karych.git"},
        	{"{\"messageType\":\"1\",\"variant\":\"10\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Kopatych.git\",\"lab\":\"3\"}","1","3","10","https://github.com/vvtatyana/Kopatych.git"},
        	{"{\"messageType\":\"1\",\"variant\":\"11\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Bibi.git\",\"lab\":\"3\"}","1","3","11","https://github.com/vvtatyana/Bibi.git"},
        	{"{\"messageType\":\"1\",\"variant\":\"12\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Mysharik.git\",\"lab\":\"3\"}","1","3","12","https://github.com/vvtatyana/Mysharik.git"},
        	{"{\"messageType\":\"1\",\"variant\":\"13\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Mulya.git\",\"lab\":\"3\"}","1","3","13","https://github.com/vvtatyana/Mulya.git"},
        	{"{\"messageType\":\"1\",\"variant\":\"14\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Zheleznaya_Nyanya.git\",\"lab\":\"3\"}","1","3","14","https://github.com/vvtatyana/Zheleznaya_Nyanya.git"},
        	{"{\"messageType\":\"1\",\"variant\":\"15\",\"link\":\"https:\\/\\/github.com\\/vvtatyana\\/Tigritsiya.git\",\"lab\":\"3\"}","1","3","15","https://github.com/vvtatyana/Tigritsiya.git"
		}});
    }
// mesType
//key
//text
//rejCode
    @Test
    public void test() {
    	Assert.assertEquals(server.TypeMessage,expectedMesType);
    	Assert.assertEquals(server.NomberLab,expectedNomerLabi);
    	Assert.assertEquals(server.NomberVar,expectedNomer);
    	Assert.assertEquals(server.Repos,expectedSilka);
    }



}