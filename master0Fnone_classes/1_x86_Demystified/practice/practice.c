/*
Author: jeFF0Falltrades

From the master0Fnone Class Reverse Engineering Series:

   GitHub: https://github.com/jeFF0Falltrades/Tutorials/tree/master/master0Fnone_classes/1_x86_Demystified

   YouTube:

MIT License

Copyright (c) 2023 Jeff Archer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#define ARR_SIZE 10

int global = 13;

typedef struct thing
{
    char c;
    int x;
    int *px;
} Thing;

typedef struct node
{
    int data;
    struct node *next;
} Node;

void print_function_header(const char *function_name)
{
    printf("****Running %s()****\n\n", function_name);
}

int quick_maths(const int x, const int y)
{
    print_function_header("quick_maths");
    int a = 3;
    int *b = (int *)malloc(sizeof(int));
    if (!b)
    {
        printf("Uh-oh, no memory left!");
        return 0;
    }
    *b = 5;
    char m = 'm';

    printf("\t%d + %d = %d\n\n", x, y, x + y);
    printf("\t%d - %d = %d\n\n", x, y, x - y);
    printf("\t%d * %d = %d\n\n", x, y, x * y);
    printf("\t%d / %d = %d\n\n", x, y, x / y);
    printf("\t%d %% %d = %d\n\n", x, y, x % y);

    printf("\t%d << 2 = %d\n\n", a, a << 2);
    printf("\t%d >> 1 = %d\n\n", global, global >> 1);
    printf("\tChars can shift too!\n\t%c << 3 = %c\n\n", m, m << 3);

    printf("\t%d & 2 = %d\n\n", *b, *b & 2);
    printf("\t%d | 2 = %d\n\n", *b, *b | 2);
    printf("\t%d ^ %d = %d\n\n", a, *b, a ^ *b);

    printf("\t%d + 2 == %d is %d\n\n", a, *b, a + 2 == *b);
    printf("\t%d == %d is %d\n\n", a, *b, a == *b);
    printf("\t%d <= %d is %d\n\n", a, *b, a <= *b);

    free(b);
    b = NULL;

    return y - x;
}

void loop_soup()
{
    print_function_header("loop_soup");
    int x = 1;
    while (x < 3)
    {
        printf("\tx is %d\n\n", x++);
    }

    for (x = 0; x <= 10; x++)
    {
        printf("\tNow x is %d\n\n", x);
    }

    do
    {
        printf("\tFinally, x is %d\n\n", ++x);
    } while (x <= 14);
    while (true)
    {
        printf("\tI'm in an infinite loop\n\n");
        x++;
        if (x != 17)
        {
            continue;
        }
        else
        {
            printf("\tx is 17 now; Time to break\n\n");
            break;
        }
    }
}

void terms_and_conditions()
{
    print_function_header("terms_and_conditions");
    bool a = true, b = false;
    printf("\ta is %s\n\n", a ? "true" : "false");
    a = b;
    printf("\tOh, actually, a is %s\n\n", a ? "true" : "false");
    a = true;
    printf("\tWait, no, a is seriously %s\n\n", a ? "true" : "false");
    printf("\ta && b is %s\n\n", a && b ? "true" : "false");
    printf("\ta || b is %s\n\n", a || b ? "true" : "false");

    printf("\tBe careful of order of operations!\n\n");
    int c = 4, d = 6;
    printf("\t%d & %d != 0 is %s\n\n", c, d, c & d != 0 ? "true" : "false");
    printf("\t(%d & %d) != 0 is %s\n\n", c, d, (c & d) != 0 ? "true" : "false");

    if (a)
    {
        printf("\tIf you see this, a is true\n\n");
    }
    if (!b)
    {
        printf("\tIf you see this, b is false\n\n");
    }
    else if (b)
    {
        printf("\tIf you see this, b is true\n\n");
    }

    if (a)
    {
        if (!b)
        {
            printf("\tIf you see this, a is true, and b is false\n\n");
        }
        else
        {
            printf("\tIf you see this, a is true, and b is true\n\n");
        }
    }

    if (a != b)
    {
        printf("\tIf you see this, a != b\n\n");
    }

    int x = 2;
    switch (x)
    {
    case 1:
        x += 1;
        break;
    case 2:
        x *= 2;
        printf("\tx doubled to %d\n\n", x);
        break;
    case 3:
        x /= 2;
        break;
    case 4:
        x -= 2;
        break;
    case 5:
    default:
        printf("\tNEVER SHOULD HAVE COME HERE!\n\n");
    }
}

void disarray(const int *passed_arr, const int passed_arr_size)
{
    print_function_header("disarray");
    int local_arr[ARR_SIZE];
    for (int i = 0; i < ARR_SIZE; i++)
    {
        printf("\tSetting array[%d] to %d\n\n", i, i + 1);
        local_arr[i] = i + 1;
    }
    if (passed_arr_size == ARR_SIZE)
    {
        for (int j = 0; j < passed_arr_size; j++)
        {
            if (passed_arr[j] == local_arr[j])
            {
                printf("\tpassed_arr[%d] == local_arr[%d] == %d\n\n", j, j, passed_arr[j]);
            }
        }
    }
    int *dynamic_arr = malloc(ARR_SIZE * sizeof(int));
    if (!dynamic_arr)
    {
        printf("Uh-oh, no memory left!");
        return;
    }
    printf("\tdynamic_arr has a size of %d\n\n", ARR_SIZE);
    int *temp_arr = realloc(dynamic_arr, ARR_SIZE * 2 * sizeof(int));
    if (!temp_arr)
    {
        printf("Uh-oh, no memory left!");
        free(dynamic_arr);
        dynamic_arr = NULL;
        return;
    }
    dynamic_arr = temp_arr;
    printf("\tNow, dynamic_arr has a size of %d\n\n", ARR_SIZE * 2);
    free(dynamic_arr);
    dynamic_arr = NULL;
}

void disappointers(char *str, const int str_size)
{
    print_function_header("disappointers");
    char *str_ptr = str;
    printf("\t");
    for (; *str_ptr; str_ptr++)
    {
        printf("%c", *str_ptr);
    }
    str_ptr = NULL;
    str[str_size - 2] = '?';
    printf("\n\t%s\n", str);
}

void struct_your_stuff()
{
    print_function_header("struct_your_stuff");
    Thing thing;
    thing.c = 'X';
    thing.x = 13;
    thing.px = &(thing.x);

    Thing thing_two;
    thing_two.c = 'O';
    thing_two.x = 7;
    thing_two.px = &(thing.x);

    thing.x = 12;
    printf("\tthing_two.x == %d\n\n", thing_two.x);
    printf("\t*thing_two.px == %d\n\n", *(thing_two.px));
}

Node *insert_at_start_of_ll(Node *head, int data)
{
    Node *new_node = (Node *)malloc(sizeof(Node));
    if (!new_node)
    {
        printf("Uh-oh, no memory left!");
        return NULL;
    }
    new_node->data = data;
    new_node->next = head;
    return new_node;
}

void linked_list_not_to_be_confused_with_zeldad_list()
{
    print_function_header("linked_list_not_to_be_confused_with_zeldad_list");
    Node *head = NULL;
    head = insert_at_start_of_ll(head, 99);
    head = insert_at_start_of_ll(head, 66);
    head = insert_at_start_of_ll(head, 33);

    Node *current = head;
    printf("\tHEAD =>");
    while (current)
    {
        printf(" %d =>", current->data);
        current = current->next;
    }
    printf(" END\n\n");

    current = head;
    Node *to_delete = NULL;
    while (current)
    {
        to_delete = current;
        current = current->next;
        printf("\tDeleting %d...\n\n", to_delete->data);
        free(to_delete);
        to_delete = NULL;
    }
}

int main()
{
    print_function_header("main");
    int x = 5, y = 7, result = 0;
    int arr[ARR_SIZE];
    for (int i = 0; i < ARR_SIZE; i++)
    {
        arr[i] = i + 1;
    }
    char str[] = "I'm a string, look at me!\n";
    int str_size = 0;
    for (str_size = 0; str[str_size] != '\0'; ++str_size)
        ;

    printf("quick_maths() result is %d\n\n", quick_maths(x, y));
    loop_soup();
    terms_and_conditions();
    disarray(arr, ARR_SIZE);
    disappointers(str, str_size);
    struct_your_stuff();
    linked_list_not_to_be_confused_with_zeldad_list();

    printf("All done!\n\n");
    getchar();
    return 0;
}