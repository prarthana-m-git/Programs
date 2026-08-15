#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void dramaticPause() {
    printf("\nThinking");
    for (int i = 0; i < 3; i++) {
        printf(".");
        fflush(stdout);
        for (volatile long j = 0; j < 100000000; j++);
    }
}

int main() {

    int choice;
    int secret, guess;
    int attempts;
    int score = 0;

    srand(time(NULL));

    printf("========================================\n");
    printf("       🤖 THE ANGRY COMPUTER 🤖\n");
    printf("========================================\n");

    printf("\nComputer: Hello, human. 😐");
    printf("\nComputer: I have prepared some challenges for you.");
    printf("\nComputer: Try not to disappoint me.\n");

    while (1) {

        printf("\n\n========== MENU ==========");
        printf("\n1. Guess My Number");
        printf("\n2. Rock Paper Scissors");
        printf("\n3. Ask the Computer a Question");
        printf("\n4. Check Your Score");
        printf("\n5. Exit");

        printf("\n\nEnter your choice: ");
        scanf("%d", &choice);

        if (choice == 1) {

            secret = rand() % 100 + 1;
            attempts = 0;

            printf("\n🤖 I have selected a number between 1 and 100.");
            printf("\n🤖 Find it if you can. 😏\n");

            while (1) {

                printf("\nYour guess: ");
                scanf("%d", &guess);

                attempts++;

                if (guess == secret) {

                    printf("\n🎉 WHAT?! YOU ACTUALLY GOT IT!");
                    printf("\nAttempts: %d", attempts);

                    score += 100 - attempts * 5;

                    if (score < 0)
                        score = 0;

                    break;

                } else if (guess < secret) {

                    printf("😂 Too small!");
                    printf("\nComputer: Even my calculator is laughing.");

                } else {

                    printf("😂 Too big!");
                    printf("\nComputer: Your guess has more confidence than accuracy.");
                }
            }

        } else if (choice == 2) {

            int user, computer;

            printf("\n1. Rock 🪨");
            printf("\n2. Paper 📄");
            printf("\n3. Scissors ✂️");

            printf("\n\nChoose: ");
            scanf("%d", &user);

            computer = rand() % 3 + 1;

            printf("\n🤖 Computer chose: ");

            if (computer == 1)
                printf("Rock 🪨");
            else if (computer == 2)
                printf("Paper 📄");
            else
                printf("Scissors ✂️");

            if (user == computer) {

                printf("\n\n😐 DRAW!");
                printf("\nComputer: We are equally confused.");

            } else if (
                (user == 1 && computer == 3) ||
                (user == 2 && computer == 1) ||
                (user == 3 && computer == 2)
            ) {

                printf("\n\n😱 NOOO! YOU WON!");
                printf("\nComputer: I demand a rematch!");
                score += 50;

            } else {

                printf("\n\n😂 YOU LOST!");
                printf("\nComputer: As expected. 😎");
                score -= 10;

                if (score < 0)
                    score = 0;
            }

        } else if (choice == 3) {

            int question;

            printf("\nAsk me something important.");
            printf("\n\n1. Are you intelligent?");
            printf("\n2. Will I become rich?");
            printf("\n3. Are you better than me?");
            printf("\n4. Do you like humans?");

            printf("\n\nChoose: ");
            scanf("%d", &question);

            dramaticPause();

            switch (question) {

            case 1:
                printf("\n\n🤖 Obviously.");
                printf("\nBut don't worry, you are improving. 😂");
                break;

            case 2:
                printf("\n\n🤖 Yes.");
                printf("\nBut first stop buying unnecessary things. 💸");
                break;

            case 3:
                printf("\n\n🤖 Next question. 😌");
                break;

            case 4:
                printf("\n\n🤖 Humans are acceptable.");
                printf("\nEspecially the ones who give me electricity. ⚡");
                break;

            default:
                printf("\n🤖 I don't understand you.");
                printf("\nComputer: Perhaps learn to use a menu first. 😂");
            }

        } else if (choice == 4) {

            printf("\n========== SCORE ==========");
            printf("\nYour score: %d", score);

            if (score >= 200)
                printf("\n🏆 Computer: Okay... you're actually good.");

            else if (score >= 100)
                printf("\n😎 Computer: Not bad, human.");

            else if (score >= 50)
                printf("\n🙂 Computer: Average performance detected.");

            else
                printf("\n😂 Computer: We need to talk about your skills.");

        } else if (choice == 5) {

            printf("\n\n🤖 Goodbye, human.");
            printf("\n🤖 Remember...");
            printf("\n🤖 I will be waiting. 👀\n");

            break;

        } else {

            printf("\n🤖 ERROR!");
            printf("\nComputer: That wasn't even one of the options. 😂");
        }
    }

    return 0;
}