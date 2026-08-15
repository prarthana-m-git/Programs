#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_ACCOUNTS 50
#define NAME_SIZE 50
#define PIN_SIZE 5
#define HISTORY_SIZE 100

typedef struct {
    int id;
    char name[NAME_SIZE];
    char pin[PIN_SIZE];
    double balance;
    char history[HISTORY_SIZE][100];
    int transactionCount;
} Account;

Account accounts[MAX_ACCOUNTS];
int accountCount = 0;

void encryptPin(char *pin) {
    for (int i = 0; pin[i] != '\0'; i++)
        pin[i] = ((pin[i] - '0' + 3) % 10) + '0';
}

void decryptPin(char *pin) {
    for (int i = 0; pin[i] != '\0'; i++)
        pin[i] = ((pin[i] - '0' + 7) % 10) + '0';
}

int findAccount(int id) {
    for (int i = 0; i < accountCount; i++) {
        if (accounts[i].id == id)
            return i;
    }

    return -1;
}

void addHistory(Account *acc, const char *message) {
    if (acc->transactionCount < HISTORY_SIZE) {
        strcpy(
            acc->history[acc->transactionCount],
            message
        );

        acc->transactionCount++;
    }
}

void createAccount() {

    if (accountCount >= MAX_ACCOUNTS) {
        printf("\nMaximum account limit reached!\n");
        return;
    }

    Account *acc = &accounts[accountCount];

    acc->id = 1000 + accountCount + 1;

    printf("\nEnter account holder name: ");
    scanf(" %[^\n]", acc->name);

    printf("Enter 4-digit PIN: ");
    scanf("%4s", acc->pin);

    for (int i = 0; i < 4; i++) {
        if (acc->pin[i] < '0' || acc->pin[i] > '9') {
            printf("\nInvalid PIN!\n");
            return;
        }
    }

    encryptPin(acc->pin);

    acc->balance = 0;
    acc->transactionCount = 0;

    addHistory(acc, "Account created");

    printf("\nAccount created successfully!");
    printf("\nAccount ID: %d\n", acc->id);

    accountCount++;
}

int login() {

    int id;
    char pin[PIN_SIZE];

    printf("\nEnter Account ID: ");
    scanf("%d", &id);

    printf("Enter PIN: ");
    scanf("%4s", pin);

    int index = findAccount(id);

    if (index == -1) {
        printf("\nAccount not found!\n");
        return -1;
    }

    char storedPin[PIN_SIZE];

    strcpy(storedPin, accounts[index].pin);
    decryptPin(storedPin);

    if (strcmp(pin, storedPin) != 0) {
        printf("\nIncorrect PIN!\n");
        return -1;
    }

    printf("\nLogin successful!\n");

    return index;
}

void deposit(Account *acc) {

    double amount;

    printf("\nEnter deposit amount: ₹");
    scanf("%lf", &amount);

    if (amount <= 0) {
        printf("\nInvalid amount!\n");
        return;
    }

    acc->balance += amount;

    char message[100];

    sprintf(
        message,
        "Deposited ₹%.2lf",
        amount
    );

    addHistory(acc, message);

    printf("\nDeposit successful!");
    printf("\nCurrent Balance: ₹%.2lf\n", acc->balance);
}

void withdraw(Account *acc) {

    double amount;

    printf("\nEnter withdrawal amount: ₹");
    scanf("%lf", &amount);

    if (amount <= 0) {
        printf("\nInvalid amount!\n");
        return;
    }

    if (amount > acc->balance) {
        printf("\nInsufficient balance!\n");
        return;
    }

    acc->balance -= amount;

    char message[100];

    sprintf(
        message,
        "Withdrawn ₹%.2lf",
        amount
    );

    addHistory(acc, message);

    printf("\nWithdrawal successful!");
    printf("\nRemaining Balance: ₹%.2lf\n", acc->balance);
}

void transfer(Account *sender) {

    int receiverID;
    double amount;

    printf("\nEnter receiver Account ID: ");
    scanf("%d", &receiverID);

    int receiverIndex = findAccount(receiverID);

    if (receiverIndex == -1) {
        printf("\nReceiver account not found!\n");
        return;
    }

    if (receiverID == sender->id) {
        printf("\nCannot transfer to the same account!\n");
        return;
    }

    printf("Enter amount: ₹");
    scanf("%lf", &amount);

    if (amount <= 0 || amount > sender->balance) {
        printf("\nInvalid amount or insufficient balance!\n");
        return;
    }

    sender->balance -= amount;
    accounts[receiverIndex].balance += amount;

    char message1[100];
    char message2[100];

    sprintf(
        message1,
        "Transferred ₹%.2lf to Account %d",
        amount,
        receiverID
    );

    sprintf(
        message2,
        "Received ₹%.2lf from Account %d",
        amount,
        sender->id
    );

    addHistory(sender, message1);
    addHistory(&accounts[receiverIndex], message2);

    printf("\nTransfer successful!\n");
}

void showHistory(Account *acc) {

    printf("\n========== TRANSACTION HISTORY ==========\n");

    if (acc->transactionCount == 0) {
        printf("No transactions available.\n");
        return;
    }

    for (int i = 0; i < acc->transactionCount; i++) {
        printf("%d. %s\n",
               i + 1,
               acc->history[i]);
    }
}

void accountMenu(Account *acc) {

    int choice;

    while (1) {

        printf("\n\n========== ACCOUNT MENU ==========");
        printf("\nWelcome, %s", acc->name);

        printf("\n\n1. Check Balance");
        printf("\n2. Deposit");
        printf("\n3. Withdraw");
        printf("\n4. Transfer Money");
        printf("\n5. Transaction History");
        printf("\n6. Logout");

        printf("\n\nEnter choice: ");
        scanf("%d", &choice);

        switch (choice) {

        case 1:
            printf("\nCurrent Balance: ₹%.2lf\n",
                   acc->balance);
            break;

        case 2:
            deposit(acc);
            break;

        case 3:
            withdraw(acc);
            break;

        case 4:
            transfer(acc);
            break;

        case 5:
            showHistory(acc);
            break;

        case 6:
            printf("\nLogged out successfully.\n");
            return;

        default:
            printf("\nInvalid choice!\n");
        }
    }
}

int main() {

    int choice;

    printf("========================================\n");
    printf("       SECURE BANKING SYSTEM\n");
    printf("========================================\n");

    while (1) {

        printf("\n\n1. Create Account");
        printf("\n2. Login");
        printf("\n3. Exit");

        printf("\n\nEnter choice: ");
        scanf("%d", &choice);

        switch (choice) {

        case 1:
            createAccount();
            break;

        case 2: {
            int index = login();

            if (index != -1)
                accountMenu(&accounts[index]);

            break;
        }

        case 3:
            printf("\nThank you for using the banking system!\n");
            return 0;

        default:
            printf("\nInvalid choice!\n");
        }
    }
}