
import org.junit.After;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;


import java.util.Arrays;
import java.util.Collection;

import static org.hamcrest.CoreMatchers.is;
import static org.junit.Assert.assertThat;

@RunWith(value = Parameterized.class)
public class SeleniumTest {

    private String url;
    private String number;
    private Selenium selen;
    private String expected;

    // Inject via constructor
    // for {8, 2, 10}, numberA = 8, numberB = 2, expected = 10
    public SeleniumTest(String url, String  number,String expected) {
        this.url=url;
        this.number=number;
        this.expected=expected;
        selen=new Selenium(url,number);
    }

    // name attribute is optional, provide an unique name for test
    // multiple parameters, uses Collection<Object[]>
    @Parameters(name = "{index}: ({0},{1}) = {2}")
    public static Collection<Object[]> data() {
        return Arrays.asList(new Object[][]{

                {"https://github.com/vvtatyana/Losiash","1", "0"},
                {"https://github.com/vvtatyana/Krosh","2","0"},
                {"https://github.com/vvtatyana/Yozhik","3","0"},
                {"https://github.com/vvtatyana/Barash","4","0"},
                {"https://github.com/vvtatyana/Nusha","5","0"},
                {"https://github.com/vvtatyana/Pin","6","0"},
                {"https://github.com/vvtatyana/Sovunya","7","0"},
                {"https://github.com/vvtatyana/Pandi","8","0"},
                {"https://github.com/vvtatyana/Kar-Karych","9","0"},
                {"https://github.com/vvtatyana/Kopatych","10","0"},
                {"https://github.com/vvtatyana/Bibi","11","0"},
                {"https://github.com/vvtatyana/Mysharik","12","0"},
                {"https://github.com/vvtatyana/Mulya", "13", "0"},
                {"https://github.com/vvtatyana/Zheleznaya_Nyanya", "14", "0"},
                {"https://github.com/vvtatyana/Tigritsiya", "15", "0"}
        });
    }

    @Test
    public void test() {
       selen.test();
        assertThat(selen.Get_Ozenka(), is(expected));
        System.out.println(selen.Get_Result());
    }



}