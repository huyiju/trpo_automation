
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
    private String expectedrez;

    // Inject via constructor
    // for {8, 2, 10}, numberA = 8, numberB = 2, expected = 10
    public SeleniumTest(String url, String  number,String expected,String expectedrez ) {
        this.url=url;
        this.number=number;
        this.expected=expected;
        this.expectedrez=expectedrez;
        selen=new Selenium(url,number);

    }

    // name attribute is optional, provide an unique name for test
    // multiple parameters, uses Collection<Object[]>
    @Parameters(name = "{index}: ({0},{1}) = {2}")
    public static Collection<Object[]> data() {
        return Arrays.asList(new Object[][]{
                  {"https://github.com/vvtatyana/Losiash","1", "0","Неверное имя репозитория\n"},
                  {"https://github.com/vvtatyana/Krosh","2","0", "Неверное имя ветки\n"},
                  {"https://github.com/vvtatyana/Yozhik","3","0","Файл Readme не найден\nВ ветке master неверное кол-во файлов\n"},
                  {"https://github.com/vvtatyana/Barash","4","0","В ветке master неверное кол-во файлов\n"},
                  {"https://github.com/vvtatyana/Nusha","5","0", "Имя labels не совпадает\nИмя открытого pull_request неверно,либо не назначен label\nИмя закрытого issues неверно\n"},
                  {"https://github.com/vvtatyana/Pin","6","0","Имя milestone некорректно\n"},
                  {"https://github.com/vvtatyana/Sovunya","7","0","Неверное имя project\n"},
                  {"https://github.com/vvtatyana/Pandi","8","0","Доска To do не содержит задачи: Внешность\nДоска In progress не содержит задачи: Предпочтения и интересы\nДоска Done не содержит задачи: Характер\nНеверное имя открытого issue/issues\n"},
                  {"https://github.com/vvtatyana/Kar-Karych","9","0","Кол-во pull_request неверно\nНе совпадает кол-во issues\nВ ветке master неверное кол-во файлов\n"},
                  {"https://github.com/vvtatyana/Kopatych","10","0","Имя открытого pull_request неверно,либо не назначен label\nНеверное имя открытого issue/issues\nВ ветке master неверные файлы\n"},
                  {"https://github.com/vvtatyana/Bibi","11","0","Доска To do не содержит задачи: Отношения с другими смешариками\nДоска Done не содержит задачи: Биография\nИмя закрытого pull_request неверно,либо не назначен label\nНеверное имя открытого issue/issues\nВ ветке master неверные файлы\n"},
                  {"https://github.com/vvtatyana/Mysharik","12","0","Кол-во pull_request неверно\nНе совпадает кол-во issues\nНеверное кол-во branches\n"},
                  {"https://github.com/vvtatyana/Mulya", "13", "0","Label верен, но назначен не на все задачи или/и pull_requests\nКол-во pull_request неверно\nНе совпадает кол-во issues\nВ ветке master неверное кол-во файлов\n"},
                  {"https://github.com/vvtatyana/Zheleznaya_Nyanya", "14", "0","Label не назначен на задачи или или/и pull_requests \nДоска To do не содержит задач.\nДоска In progress не содержит задач.\nДоска Done не содержит задач.\nКол-во pull_request неверно\nНе совпадает кол-во issues\nВ ветке master неверное кол-во файлов\n" },
                  {"https://github.com/vvtatyana/Tigritsiya", "15", "0","Кол-во pull_request неверно\nНе совпадает кол-во issues\nНеверное кол-во branches\n"},
                  {"https://github.com/HozookiSan/Tigritsiya","15","1","Работа сдана\n"},
        });
    }

    @Test
    public void test() {
        selen.test();
        assertThat(selen.Get_Ozenka(), is(expected));
        assertThat(selen.Get_Result(), is(expectedrez));
        System.out.println(selen.Get_Result());
    }



}