#include<arpa/inet.h>
#include<unistd.h>
#include<sys/socket.h>
#include<sys/types.h>
#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<yajl/yajl_tree.h>
int main()
{
    int sockfd,n,sockffd,nn;
    struct sockaddr_in servaddr,sservaddr;
    char dest_ip[] = "127.0.0.1";
    int dest_port = 5566;
    char recvline[1000];
    char buff[100];
    sockfd=socket(AF_INET,SOCK_DGRAM,0);
    bzero(&servaddr,sizeof(servaddr)); 
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr=inet_addr(dest_ip);
    servaddr.sin_port=htons(dest_port);
 
    int bottom = 3000, top=60000, mid=0;
    for(;;)
    {
        mid = (bottom + top)/2;
        snprintf(buff,100,"{'guess':%d}",mid);
        sendto(sockfd,buff,strlen(buff),0,(struct sockaddr *)&servaddr,sizeof(servaddr));
        printf("send {'guess':%d}\n",mid);
        n=recvfrom(sockfd,recvline,10000,0,NULL,NULL);
        recvline[n]=0;
        printf("receive ");
        printf("%s\n",recvline);
        if(recvline[11]=='l')
        {
            bottom = mid;
            continue;
        }
        else if(recvline[11]=='s')
        {
            top = mid;
            continue;
        }
        else if(recvline[11]=='b')
        {
            sockffd=socket(AF_INET,SOCK_DGRAM,0);
            bzero(&sservaddr,sizeof(sservaddr)); 
            sservaddr.sin_family = AF_INET;
            sservaddr.sin_addr.s_addr=inet_addr(dest_ip);
            sservaddr.sin_port=htons(mid);
            char ans[] = "{'student_id':'0216003'}";
            sendto(sockffd,ans,strlen(ans),0,
              (struct sockaddr *)&sservaddr,sizeof(sservaddr));
            printf("send ");
            printf("%s\n",ans);
            nn=recvfrom(sockffd,recvline,10000,0,NULL,NULL);
            recvline[nn]=0;
            close(sockffd);

            return 0;
        }
        else
            return 1;
    }
    close(sockfd);
}

