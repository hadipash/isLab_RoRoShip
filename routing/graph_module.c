/*161022*/
//#include <python2.7/Python.h>
#include <Python.h>
#include <numpy/arrayobject.h>
#include <math.h>
#include <stdbool.h>

#define not_available 1
#define available 0
#define MAX 250
#define MAX_Q MAX*MAX*16
#define UP 0
#define RIGHT 1
#define DOWN 2
#define LEFT 3
#define FILE_PATH "../routing/path_list"

int grid[MAX][MAX];
int vertex[MAX][MAX][2];
int curve[MAX][MAX][8][2];
int temp[MAX][MAX];
int grid_width=MAX, grid_height=MAX;
int type_width, type_height, type_inner_r, type_outer_r, type_minR, type_radius, path_print, type_bump;
double type_Fmin_R;
long long small_r_sqr, large_r_sqr, large_r_sqr2;
int dx[4] = {0,0,1,1};
int dy[4] = {0,1,0,1};

bool check_down_right(int top_x, int top_y, int inner_r, int outer_r, int width, int height);
bool check_up_right(int top_x, int top_y, int inner_r, int outer_r, int width, int height);
bool check_down_left(int top_x, int top_y, int inner_r, int outer_r, int width, int height);
bool check_up_left(int top_x, int top_y, int inner_r, int outer_r, int width, int height);
bool check_left_up(int top_x, int top_y, int inner_r, int outer_r, int width, int height);
bool check_right_up(int top_x, int top_y, int inner_r, int outer_r, int width, int height);
bool check_left_down(int top_x, int top_y, int inner_r, int outer_r, int width, int height);
bool check_right_down(int top_x, int top_y, int inner_r, int outer_r, int width, int height);
long long lsqr(int x) {
    return 1ll*x*x;
}
bool judge_in_and_check(int center_x, int center_y, int i, int j) {
    long long large_r = lsqr(center_x - j) + lsqr(center_y - i) - lsqr(type_minR);
    long long small_r = lsqr(center_x - j) + lsqr(center_y - i) - lsqr(type_radius - type_width);
    if(i < 0 || j < 0 || i >= grid_height || j >= grid_width) 
        return 0;
    if(large_r <= 0 && small_r >= 0) {
        if(center_y==20&&type_radius+1==center_x)
                printf("O");
        if(grid[j][i] == not_available)
            return 0;
    }
    return 1;
}
bool down_right(int top_left_x, int top_left_y, int dest_x, int dest_y) {
    int center_x = dest_x + type_bump;
    int center_y = top_left_y + type_bump;
    //type_minR = sqrt(lsqr(center_x - top_left_x) + lsqr(type_height)) + 0.999;

    //if(top_left_y==1&&top_left_x==1)
    //    printf("topx: %d, topy: %d, center_x: %d, center_y: %d\n",top_left_x, top_left_y,center_x,center_y);

    /*///////////////////////////////////////
    o--o---------x              x
    |--|       /                |   \
    |--|     /                  o------o
    |--|   /                    |------|
    o--o/                       o------o
    ///////////////////////////////////////*/
    int i,j,k;
    //if(center_y==20&&type_radius+1==center_x)
    //    printf("\n\n");

    int chk_height_bgn = center_y - type_bump;
    int chk_height_end = center_y + type_minR;
    int chk_width_bgn = center_x - type_minR;
    int chk_width_end = center_x + type_height - type_bump;

    for(i = chk_height_bgn; i <= chk_height_end; i++) {
        for(j = chk_width_bgn; j <= chk_width_end; j++) {
            //if(center_y==20&&type_radius+1==center_x)
            //    printf("\t%d %d",j,i);
            if(i <= center_y && j >= top_left_x + type_width)
                continue;
            if(i <= dest_y && j >= dest_x + type_bump)
                continue;
            if(i < 0 || j < 0)
                return 0;
            for(k=0;k<4;k++) {
                long long cur_r_sqr = lsqr(j - center_x + dx[k]) + lsqr(i - center_y + dy[k]);
                if(small_r_sqr <= cur_r_sqr && (cur_r_sqr <= large_r_sqr || cur_r_sqr <= large_r_sqr2)) {
                    if(j + dx[k] >= grid_width || i + dy[k] >= grid_height)
                        return 0;
                    if(grid[j][i] == not_available)
                        return 0;
                }
                //if(center_y==20&&type_radius+1==center_x)
                //    printf("O");
            }
    //        if(!judge_in_and_check(center_x, center_y, i, j))
    //            return 0;
        }
        //if(center_y==20&&type_radius+1==center_x)
        //    printf("\n");
    }
    return 1;
}
bool up_right(int top_left_x, int top_left_y, int dest_x, int dest_y) {
    int center_x = top_left_x + type_radius;
    int center_y = top_left_y + type_height - type_bump;
    //type_minR = sqrt(lsqr(center_x - top_left_x) + lsqr(type_height)) + 0.999;

    /*///////////////////////////////////////
    o--o                        o------o
    |--|  \                     |------|
    |--|     \                  o------o
    |--|        \               |   /
    o--o---------x              x
    ///////////////////////////////////////*/
    int i,j,k;

    int chk_height_bgn = center_y - type_minR;
    int chk_height_end = center_y + type_bump;
    int chk_width_bgn = center_x - type_minR;
    int chk_width_end = center_x + type_height - type_bump;
    //if(center_y==20&&type_radius+1==center_x)
    //    printf("\n\n");
    for(i = chk_height_bgn; i <= chk_height_end; i++) {
        for(j = chk_width_bgn; j <= chk_width_end; j++) {
            //if(center_y==20&&type_radius+1==center_x)
            //    printf("\t%d %d",j,i);
            if(i >= center_y && j >= top_left_x + type_width)
                continue;
            if(i >= dest_y + type_width && j >= center_x)
                continue;
            if(i < 0 || j < 0)
                return 0;
            for(k=0;k<4;k++) {
                long long cur_r_sqr = lsqr(j - center_x + dx[k]) + lsqr(i - center_y + dy[k]);
                if(small_r_sqr <= cur_r_sqr && (cur_r_sqr <= large_r_sqr || cur_r_sqr <= large_r_sqr2)) {
                    if(j + dx[k] >= grid_width || i + dy[k] >= grid_height)
                        return 0;
                    if(grid[j][i] == not_available)
                        return 0;
            }
            //    if(center_y==20&&type_radius+1==center_x)
            //        printf("O");
            }
    //        if(!judge_in_and_check(center_x, center_y, i, j))
    //            return 0;
        }
        //if(center_y==20&&type_radius+1==center_x)
        //    printf("\n");
    }
    return 1;
}
bool down_left(int top_left_x, int top_left_y, int dest_x, int dest_y) {
    int center_x = top_left_x + type_width - type_radius;
    int center_y = top_left_y + type_bump;
    //type_minR = sqrt(lsqr(center_x - (top_left_x + type_width)) + lsqr(type_height)) + 0.999;

    /*///////////////////////////////////////
    x---------o--o                     x
      \       |--|                  /   |
         \    |--|               o------o
            \ |--|               |------|
              o--o               o------o
    ///////////////////////////////////////*/

    int i,j,k;

    int chk_height_bgn = center_y - type_bump;
    int chk_height_end = center_y + type_minR;
    int chk_width_bgn = center_x - type_height + type_bump;
    int chk_width_end = center_x + type_minR;//(int)(type_radius + 0.9999);
    //if(center_y==20&&type_radius+1==center_x)
    //    printf("s : %d %d-> dest %d %d\n\n",top_left_x,top_left_y,dest_x,dest_y);
    for(i = chk_height_bgn; i <= chk_height_end; i++) {
        for(j = chk_width_bgn; j <= chk_width_end; j++) {
            //if(center_y==20&&type_radius+1==center_x)
            //    printf("\t%d %d",j,i);
            if(j <= center_x && i <= dest_y)
                continue;
            if(j <= top_left_x && i <= center_y)
                continue;
            if(i < 0 || j < 0)
                return 0;
            for(k=0;k<4;k++) {
                long long cur_r_sqr = lsqr(j - center_x + dx[k]) + lsqr(i - center_y + dy[k]);
                if(small_r_sqr <= cur_r_sqr && (cur_r_sqr <= large_r_sqr || cur_r_sqr <= large_r_sqr2)) {
                    if(j + dx[k] >= grid_width || i + dy[k] >= grid_height)
                        return 0;
                    if(grid[j][i] == not_available)
                        return 0;
                }
                //if(center_y==20&&type_radius+1==center_x)
                //    printf("O");
            }
        }
        //if(center_y==20&&type_radius+1==center_x)
        //    printf("\n");
    }
    return 1;
}
bool up_left(int top_left_x, int top_left_y, int dest_x, int dest_y) {
    int center_x = dest_x + type_height - type_bump;
    int center_y = top_left_y + type_height - type_bump;
    //type_minR = sqrt(lsqr(center_x - (top_left_x + type_width)) + lsqr(type_height)) + 0.999;

    /*///////////////////////////////////////
              o--o               o------o
           /  |--|               |------|
        /     |--|               o------o
      /       |--|                  \   |
    x---------o--o                      x
    ///////////////////////////////////////*/
    int i,j,k;

    //int chk_height_bgn = top_left_y;
    int chk_height_bgn = center_y - type_minR;
    int chk_height_end = center_y + type_bump;
    int chk_width_bgn = center_x - type_height + type_bump;
    int chk_width_end = center_x + type_minR;
    //if(center_y==20&&type_radius+1==center_x)
    //    printf("\n\n");
    for(i = chk_height_bgn; i <= chk_height_end; i++) {
        for(j = chk_width_bgn; j <= chk_width_end; j++) {
    //     if(center_y==20&&type_radius+1==center_x)
    //         printf("\t%d %d",j,i);
            if(j <= center_x && i >= dest_y+type_width)
                continue;
            if(j <= top_left_x && i >= top_left_y)
                continue;
            if(i < 0 || j < 0)
                return 0;
            for(k=0;k<4;k++) {
            long long cur_r_sqr = lsqr(j - center_x + dx[k]) + lsqr(i - center_y + dy[k]);
                if(small_r_sqr <= cur_r_sqr && (cur_r_sqr <= large_r_sqr || cur_r_sqr <= large_r_sqr2)) {
                    if(j + dx[k] >= grid_width || i + dy[k] >= grid_height)
                        return 0;
                    if(grid[j][i] == not_available)
                        return 0;
    //                if(center_y==20&&type_radius+1==center_x)
    //                    printf("!");
                }
            }
        }
    //    if(center_y==20&&type_radius+1==center_x)
    //        printf("\n");
    }
    return 1;
}
bool left_up(int top_left_x, int top_left_y, int dest_x, int dest_y) {
    int center_x = dest_x + type_radius;
    int center_y = dest_y + type_height - type_bump;
    //type_minR = sqrt(lsqr(center_x - top_left_x) + lsqr(type_radius)) + 0.999;

    /*///////////////////////////////////////
           x               o--o                  
        /  |               |--|  \
    o------o               |--|     \
    |------|               |--|        \
    o------o               o--o---------x 
    ///////////////////////////////////////*/

    int i,j,k;

    int chk_height_bgn = center_y - type_height + type_bump;
    int chk_height_end = center_y + type_minR;
    int chk_width_bgn = center_x - type_minR;
    int chk_width_end = center_x + type_bump;
    //if(center_y==20&&type_radius+1==center_x)
    //    printf("\n\n");
    for(i = chk_height_bgn; i <= chk_height_end; i++) {
        for(j = chk_width_bgn; j <= chk_width_end; j++) {
            //if(center_y==20&&type_radius+1==center_x)
            //    printf("\t%d %d",j,i);
            if(j >= dest_x + type_width && i <= center_y)
                continue;
            if(j >= center_x && i <= top_left_y)
                continue;
            if(i < 0 || j < 0)
                return 0;
            for(k=0;k<4;k++) {
                long long cur_r_sqr = lsqr(j - center_x + dx[k]) + lsqr(i - center_y + dy[k]);
                if(small_r_sqr <= cur_r_sqr && (cur_r_sqr <= large_r_sqr || cur_r_sqr <= large_r_sqr2)) {
                    if(j + dx[k] >= grid_width || i + dy[k] >= grid_height)
                        return 0;
                    if(grid[j][i] == not_available)
                        return 0;
                }
                //if(center_y==20&&type_radius+1==center_x)
                //    printf("O");
            }
        }
        //if(center_y==20&&type_radius+1==center_x)
        //    printf("\n");
    }
    /*
    int i,j,k;
    for(i = center_y; i <= center_y + type_minR - 1; i++) {//i = center_y - type_height + 1//center_y + type_minR - 1
        for(j = center_x - type_minR + 1; j <= center_x; j++) {
            if(!judge_in_and_check(center_x, center_y, i, j))
                return 0;
        }
    }*/
    return 1;
}
bool right_up(int top_left_x, int top_left_y, int dest_x, int dest_y) {
    int center_x = top_left_x + type_bump;
    int center_y = dest_y + type_height - type_bump;
    //type_minR = sqrt(lsqr(type_height) + lsqr(type_radius)) + 0.999;

    /*///////////////////////////////////////
    x                                 o--o                  
    |   \                          /  |--|
    o------o                    /     |--|
    |------|                  /       |--|
    o------o               x---------o--o 
    ///////////////////////////////////////*/
    /*int i,j,k;
    for(i = center_y - type_minR + 1; i <= center_y ; i++) {//center_y + type_height - 1
        for(j = center_x; j <= center_x + type_minR - 1; j++) {//center_x + type_minR
            if(!judge_in_and_check(center_x, center_y, i, j))
                return 0;
        }
    }*/
    int i,j,k;

    int chk_height_bgn = center_y - type_height + type_bump;
    int chk_height_end = center_y + type_minR;
    int chk_width_bgn = center_x - type_bump;
    int chk_width_end = center_x + type_minR;
    
    //if(center_y==20&&type_radius+1==center_x)
    //    printf("\n\n");
    for(i = chk_height_bgn; i <= chk_height_end; i++) {
        for(j = chk_width_bgn; j <= chk_width_end; j++) {
            //if(center_y==20&&type_radius+1==center_x)
            //    printf("\t%d %d",j,i);
            if(j <= dest_x && i <= center_y)
                continue;
            if(j <= center_x && i <= top_left_y)
                continue;
            if(i < 0 || j < 0)
                return 0;
            for(k=0;k<4;k++) {
                long long cur_r_sqr = lsqr(j - center_x + dx[k]) + lsqr(i - center_y + dy[k]);
                if(small_r_sqr <= cur_r_sqr && (cur_r_sqr <= large_r_sqr || cur_r_sqr <= large_r_sqr2)) {
                    if(j + dx[k] >= grid_width || i + dy[k] >= grid_height)
                            return 0;
                    if(grid[j][i] == not_available)
                        return 0;
                }
                //if(center_y==20&&type_radius+1==center_x)
                //    printf("O");
            }
        }
        //if(center_y==20&&type_radius+1==center_x)
        //    printf("\n");
    }
    return 1;
}
bool left_down(int top_left_x, int top_left_y, int dest_x, int dest_y) {
    int center_x = top_left_x + type_height - type_bump;
    int center_y = dest_y + type_bump;
    //type_minR = sqrt(lsqr(type_height) + lsqr(type_radius)) + 0.999;

    /*///////////////////////////////////////
    o------o             o--o---------x                                     
    |------|             |--|        /
    o------o             |--|     /
        \  |             |--|  /
           x             o--o 
    ///////////////////////////////////////*/

    int i,j,k;

    int chk_height_bgn = center_y - type_minR;
    int chk_height_end = center_y + type_height - type_bump;
    int chk_width_bgn = center_x - type_minR;
    int chk_width_end = center_x + type_bump;
    
    //if(center_y==20&&type_radius+1==center_x)
    //    printf("\n\n");
    for(i = chk_height_bgn; i <= chk_height_end; i++) {
        for(j = chk_width_bgn; j <= chk_width_end; j++) {
            //if(center_y==20&&type_radius+1==center_x)
            //    printf("\t%d %d",j,i);
            if(j >= dest_x + type_width && i >= center_y)
                continue;
            if(j >= center_x && i >= top_left_y + type_width)
                continue;
            if(i < 0 || j < 0)
                return 0;
            for(k=0;k<4;k++) {
                long long cur_r_sqr = lsqr(j - center_x + dx[k]) + lsqr(i - center_y + dy[k]);
                if(small_r_sqr <= cur_r_sqr && (cur_r_sqr <= large_r_sqr || cur_r_sqr <= large_r_sqr2)) {
                    if(j + dx[k] >= grid_width || i + dy[k] >= grid_height)
                        return 0;
                    if(grid[j][i] == not_available)
                        return 0;
                }
                //if(center_y==20&&type_radius+1==center_x)
                //    printf("O");
            }
        }
        //if(center_y==20&&type_radius+1==center_x)
        //    printf("\n");
    }

    /*
    int i,j,k;
    for(i = center_y - type_minR + 1; i <= center_y; i++) {//center_y + type_height - 1
        for(j = center_x - type_minR + 1; j <= center_x; j++) {
            if(!judge_in_and_check(center_x, center_y, i, j))
                return 0;
        }
    }*/
    return 1;
}
bool right_down(int top_left_x, int top_left_y, int dest_x, int dest_y) {
    int center_x = top_left_x + type_bump;
    int center_y = dest_y + type_bump;
    //type_minR = sqrt(lsqr(type_radius) + lsqr(type_height)) + 0.999;
    
    /*///////////////////////////////////////
    o------o             x---------o--o                                     
    |------|                \      |--| 
    o------o                  \    |--| 
    |   /                        \ |--| 
    x                              o--o 
    ///////////////////////////////////////*/
    int i,j,k;

    int chk_height_bgn = center_y - type_minR;
    int chk_height_end = center_y + type_height - type_bump;
    int chk_width_bgn = center_x - type_bump;
    int chk_width_end = center_x + type_minR;
    //if(center_y==20&&type_radius+1==center_x)
    //    printf("\n\n");
    for(i = chk_height_bgn; i <= chk_height_end; i++) {
        for(j = chk_width_bgn; j <= chk_width_end; j++) {
            //if(center_y==20&&type_radius+1==center_x)
            //    printf("\t%d %d",j,i);
            if(j <= dest_x && i >= center_y)
                continue;
            if(j <= center_x && i >= top_left_y + type_width)
                continue;
            if(i < 0 || j < 0)
                return 0;
            for(k=0;k<4;k++) {
                long long cur_r_sqr = lsqr(j - center_x + dx[k]) + lsqr(i - center_y + dy[k]);
                if(small_r_sqr <= cur_r_sqr && (cur_r_sqr <= large_r_sqr || cur_r_sqr <= large_r_sqr2)) {
                    if(j + dx[k] >= grid_width || i + dy[k] >= grid_height)
                            return 0;
                    if(grid[j][i] == not_available)
                        return 0;
                }
                //if(center_y==20&&type_radius+1==center_x)
                //    printf("O");
            }
        }
        //if(center_y==20&&type_radius+1==center_x)
        //    printf("\n");
    }
    /*int i,j,k;
    for(i = center_y - type_minR + 1; i <= center_y ; i++) {//center_y + type_height - 1
        for(j = center_x; j <= center_x + type_minR - 1; j++) {//center_x + type_minR - 1
            if(!judge_in_and_check(center_x, center_y, i, j))
                return 0;
        }
    }*/
    return 1;
}

void init() {

    int i,j,l,p,k;
    /*
    for(i=0;i<grid_width;i++) {
        for(j=0;j<grid_height;j++)
            if(i && j)
                acc[i][j] = acc[i-1][j] + acc[i][j-1] - acc[i-1][j-1] + !grid[i][j];
            else
                acc[i][j] = !grid[i][j];
    }
    for(i=0;i<grid_width;i++) {
        for(j=0;j<grid_height;j++) {
            vertex[i][j][0] = not_available;
            vertex[i][j][1] = not_available;    
            int t1 = i-type_width;
            int t2 = j-type_height; 
            if(t1 > 0 && t2 > 0)
                if(acc[i][j] - acc[t1-1][j] - acc[i][t2-1] + acc[t1-1][t2-1] == 0)
                    vertex[t1][t2][0] = available;
            else {
                int p_sum = 0;
                for(l=0;l<type_width;l++)
                    for(p=0;p<type_height;p++)
                        p_sum += grid[i+l][j+p];
                if(p_sum == 0)
                    vertex[i][j][0] = available;
            }
            t1 = i-type_height;
            t2 = j-type_width; 
            if(t1 > 0 && t2 > 0)
                if(acc[i][j] - acc[t1-1][j] - acc[i][t2-1] + acc[t1-1][t2-1] == 0)
                    vertex[t1][t2][1] = available;
            else {
                int p_sum = 0;
                for(l=0;l<type_height;l++)
                    for(p=0;p<type_width;p++)
                        p_sum += grid[i+l][j+p];
                if(p_sum == 0)
                    vertex[i][j][1] = available;
            }

        }//(int top_x, int top_y, int inner_r, int outer_r, int width, int height)
    }
    */

    /*----------------------------
    accumulate grid [x:x+type_width][y:y+type_height], if it is 0, there is no obstacle
    ------------------------------*/
    
    for(i=0;i<grid_width;i++) {
        for(j=0;j<grid_height;j++) {
            vertex[i][j][0] = not_available;
            vertex[i][j][1] = not_available;
            int p_sum_0 = 0, p_sum_1 = 0;
            for(l=0;l<type_height;l++) {
                for(p=0;p<type_width;p++) {
                    if(i + l < grid_width && j + p < grid_height)
                        p_sum_1 += grid[i+l][j+p];
                    else
                        p_sum_1 = 999;
                    if(i+p < grid_width && j+l < grid_height)
                        p_sum_0 += grid[i+p][j+l];
                    else
                        p_sum_0 = 999;
                }
            }
            if(p_sum_0 == 0)
                vertex[i][j][0] = available;
            if(p_sum_1 == 0)
                vertex[i][j][1] = available;
        }
    }
    /*----------------------------
    vertex[][] making end
    ------------------------------*/
    /*----------------------------
    accumulate grid area in curves, if it is 0, there is no obstacle
    down means from (x, y) to (x, y + a)
    right means from (x, y) to (x + a, y)
    ------------------------------*/

    for(i=0;i<grid_width;i++) {
        //printf("%d, %d", i,j);
        for(j=0;j<grid_height;j++) {
            for(k=0;k<8;k++){
                curve[i][j][k][0] = -1;
                curve[i][j][k][1] = -1;
            }
            //int ccc=0;
            int t1, t2;

            if(vertex[i][j][0] == available) {
                t1 = i + (type_radius) - (type_bump);
                t2 = j + (type_bump) + (type_radius) - (type_width);

                if(down_right(i,j,t1,t2) && vertex[t1][t2][1] == available) {
                    curve[i][j][0][0] = t1, curve[i][j][0][1] = t2;                
                }
                t1 = i + (type_width) - (type_radius) - (type_height) + (type_bump);
                t2 = j + (type_bump) + (type_radius) - (type_width);
                
                if(down_left(i,j,t1,t2) && vertex[t1][t2][1] == available) {
                    curve[i][j][1][0] = t1, curve[i][j][1][1] = t2;    
                }
                t1 = i + (type_radius) - (type_bump);
                t2 = j + (type_height) - (type_bump) - (type_radius);
                
                if(up_right(i,j,t1,t2) && vertex[t1][t2][1] == available) {
                    curve[i][j][2][0] = t1, curve[i][j][2][1] = t2; 
                }
                t1 = i + (type_width) - (type_radius) - (type_height) + (type_bump);
                t2 = j + (type_height) - (type_bump) - (type_radius);
                
                if(up_left(i,j,t1,t2) && vertex[t1][t2][1] == available) {
                    curve[i][j][3][0] = t1, curve[i][j][3][1] = t2;                     
                }
            }
            if(vertex[i][j][1] == available) {
                t1 = i + (type_bump) + (type_radius) - (type_width);
                t2 = j + (type_width) - (type_radius) - (type_height) + (type_bump);

                if(right_up(i,j,t1,t2) && vertex[t1][t2][0] == available) {
                    curve[i][j][4][0] = t1, curve[i][j][4][1] = t2;                     
                }
                t1 = i + (type_bump) + (type_radius) - (type_width);
                t2 = j + (type_radius) - (type_bump);

                if(right_down(i,j,t1,t2) && vertex[t1][t2][0] == available) {
                    curve[i][j][5][0] = t1, curve[i][j][5][1] = t2;                     
                }
                t1 = i + (type_height) - (type_bump) - (type_radius);
                t2 = j + (type_width) - (type_radius) - (type_height) + (type_bump);

                if(left_up(i,j,t1,t2) && vertex[t1][t2][0] == available) {
                    curve[i][j][6][0] = t1, curve[i][j][6][1] = t2;                     
                }
                t1 = i + (type_height) - (type_bump) - (type_radius);
                t2 = j + (type_radius) - (type_bump);

                if(left_down(i,j,t1,t2) && vertex[t1][t2][0] == available) {
                    curve[i][j][7][0] = t1, curve[i][j][7][1] = t2;                     
                }
            }
        }
    }

    /*----------------------------
    curve[][] making end
    ------------------------------*/
    /*
    for (i=0;i<50;i++){
        for (j=0; j<50;j++){
            for(k=0;k<8;k++){
                printf("%d %d | ",curve[i][j][k][0], curve[i][j][k][1]);
            }
        }
        printf("\n");
    }
    */
    return 0;
}

int ent_orientation = 0, qx[MAX_Q],qy[MAX_Q],qo[MAX_Q], size=0;
int chk_d[MAX][MAX][4][4];

void q_push(int x, int y,int next_orientation, int from_x, int from_y, int before_orientation) 
{
    qx[size] = x;
    qy[size] = y;
    qo[size] = next_orientation;
    size++;
    chk_d[x][y][next_orientation][0] = from_x;
    chk_d[x][y][next_orientation][1] = from_y;
    chk_d[x][y][next_orientation][2] = before_orientation;
    //chk_d[x][y][next_orientation][3] = value;
}

bool find_path(int x,int y,int ent_x, int ent_y, int dest_orientation, int _print) 
{
    int i,j,k,p;
    size = 0;
    q_push(ent_x, ent_y, ent_orientation, ent_x, ent_y, ent_orientation);
    //printf("%d %d \n\n",ent_x,ent_y);

    for(i=0;i<size;i++) {
        int cx = qx[i], cy = qy[i], co = qo[i];//cur_x, y, o
        //printf("x: %d   y: %d   ori: %d\n",cx,cy,co);
        int curve_x, curve_y;
        if(co == 0) { //UPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUPUP
            for(j=1;j+cy <= grid_height - type_height && chk_d[cx][cy + j][co][0] == -1 && vertex[cx][cy+j][co] == available; j++)
                q_push(cx,cy+j,co, cx, cy, 0);
            for(j=1;cy-j >= 0 && chk_d[cx][cy-j][co][0] == -1 && vertex[cx][cy-j][co] == available; j++)
                q_push(cx,cy-j,co, cx, cy, 0);
            //0 : down_right
            curve_x = curve[cx][cy][0][0], curve_y = curve[cx][cy][0][1];
            if(chk_d[curve_x][curve_y][3][0] == -1 && curve_x >= 0 && curve_y >= 0)
                q_push(curve_x, curve_y, 3, cx, cy, 0);
            //1 : down_left
            curve_x = curve[cx][cy][1][0], curve_y = curve[cx][cy][1][1];
            if(chk_d[curve_x][curve_y][1][0] == -1 && curve_x >= 0 && curve_y >= 0)
                q_push(curve_x, curve_y, 1, cx, cy, 0);
            //2 : up_right
            curve_x = curve[cx][cy][2][0], curve_y = curve[cx][cy][2][1];
            if(chk_d[curve_x][curve_y][1][0] == -1 && curve_x >= 0 && curve_y >= 0)
                    q_push(curve_x, curve_y, 1, cx, cy, 0); // RIGHT = 1
            //3 : up_left
            curve_x = curve[cx][cy][3][0], curve_y = curve[cx][cy][3][1];
            if(chk_d[curve_x][curve_y][3][0] == -1 && curve_x >= 0 && curve_y >= 0)
                    q_push(curve_x, curve_y, 3, cx, cy, 0); // LEFT = 3
        }
        if(co == 1) { //RIGHTRIGHTRIGHTRIGHTRIGHTRIGHTRIGHT
            for(j=1;cx - j >= 0 && chk_d[cx-j][cy][co][0] == -1 && vertex[cx-j][cy][co] == available; j++)
                q_push(cx-j,cy,co, cx, cy, 1);
            for(j=1;cx + j <= grid_width - type_height && chk_d[cx + j][cy][co][0] == -1 && vertex[cx+j][cy][co] == available; j++) //
                q_push(cx+j,cy,co, cx, cy, 1);
            //4 : right_up
            curve_x = curve[cx][cy][4][0], curve_y = curve[cx][cy][4][1];
            if(chk_d[curve_x][curve_y][0][0] == -1 && curve_x >= 0 && curve_y >= 0)
                q_push(curve_x, curve_y, 0, cx, cy, 1);
            //5 : right_down
            curve_x = curve[cx][cy][5][0], curve_y = curve[cx][cy][5][1];
            if(chk_d[curve_x][curve_y][2][0] == -1 && curve_x >= 0 && curve_y >= 0)
                q_push(curve_x, curve_y, 2, cx, cy, 1);
            //6 : left_up
            curve_x = curve[cx][cy][6][0], curve_y = curve[cx][cy][6][1];
            if(chk_d[curve_x][curve_y][2][0] == -1 && curve_x >= 0 && curve_y >= 0)
                q_push(curve_x, curve_y, 2, cx, cy, 1);
            //7 : left_down
            curve_x = curve[cx][cy][7][0], curve_y = curve[cx][cy][7][1];
            if(chk_d[curve_x][curve_y][0][0] == -1 && curve_x >= 0 && curve_y >= 0)
                q_push(curve_x, curve_y, 0, cx, cy, 1);
        }
        if(co == 2) { //DOWNDOWNDOWNDOWNDOWNDOWNDOWNDOWNDOWN
            for(j=1;cy + j <= grid_height - type_height && chk_d[cx][cy + j][co][0] == -1 && vertex[cx][cy + j][co-2] == available; j++) //
                q_push(cx,cy+j,co, cx, cy, 2);
            for(j=1;cy - j >= 0 && chk_d[cx][cy-j][co][0] == -1 && vertex[cx][cy-j][co-2] == available; j++)
                q_push(cx,cy-j,co, cx, cy, 2);
            //0 : down_right
            curve_x = curve[cx][cy][0][0], curve_y = curve[cx][cy][0][1];
            if(chk_d[curve_x][curve_y][1][0] == -1 && curve_x >= 0 && curve_y >= 0)
                q_push(curve_x, curve_y, 1, cx, cy, 2);
            //1 : down_left
            curve_x = curve[cx][cy][1][0], curve_y = curve[cx][cy][1][1];
            if(chk_d[curve_x][curve_y][3][0] == -1 && curve_x >= 0 && curve_y >= 0)
                q_push(curve_x, curve_y, 3, cx, cy, 2);
            //2 : up_right
            curve_x = curve[cx][cy][2][0], curve_y = curve[cx][cy][2][1];
            if(chk_d[curve_x][curve_y][3][0] == -1 && curve_x >= 0 && curve_y >= 0)
                    q_push(curve_x, curve_y, 3, cx, cy, 2); // RIGHT = 1
            //3 : up_left
            curve_x = curve[cx][cy][3][0], curve_y = curve[cx][cy][3][1];
            if(chk_d[curve_x][curve_y][1][0] == -1 && curve_x >= 0 && curve_y >= 0)
                    q_push(curve_x, curve_y, 1, cx, cy, 2); // LEFT = 3
        }
        if(co == 3) { //LEFTLEFTLEFTLEFTLEFTLEFTLEFTLEFTLEFT
            for(j=1;cx - j >= 0 && chk_d[cx-j][cy][co][0] == -1 && vertex[cx-j][cy][co-2] == available; j++)
                q_push(cx-j,cy,co, cx, cy, 3);
            for(j=1;cx + j <= grid_width - type_height && chk_d[cx + j][cy][co][0] == -1 && vertex[cx+j][cy][co-2] == available; j++) //
                q_push(cx+j,cy,co, cx, cy, 3);
            //4 : right_up
            curve_x = curve[cx][cy][4][0], curve_y = curve[cx][cy][4][1];
            if(chk_d[curve_x][curve_y][2][0] == -1 && curve_x >= 0 && curve_y >= 0)
                q_push(curve_x, curve_y, 2, cx, cy, 3);
            //5 : right_down
            curve_x = curve[cx][cy][5][0], curve_y = curve[cx][cy][5][1];
            if(chk_d[curve_x][curve_y][0][0] == -1 && curve_x >= 0 && curve_y >= 0)
                q_push(curve_x, curve_y, 0, cx, cy, 3);
            //6 : left_up
            curve_x = curve[cx][cy][6][0], curve_y = curve[cx][cy][6][1];
            if(chk_d[curve_x][curve_y][0][0] == -1 && curve_x >= 0 && curve_y >= 0)
                q_push(curve_x, curve_y, 0, cx, cy, 3);
            //7 : left_down
            curve_x = curve[cx][cy][7][0], curve_y = curve[cx][cy][7][1];
            if(chk_d[curve_x][curve_y][2][0] == -1 && curve_x >= 0 && curve_y >= 0)
                q_push(curve_x, curve_y, 2, cx, cy, 3);
        }
    }
    /*
        printf("\n");
        printf("\n");
    for(i=0;i<80;i++) {
        for(j=0;j<50;j++)
            printf("%d",chk_d[i][j][0]);
        printf("\n");
    }
        printf("\n");
    for(i=0;i<80;i++) {
        for(j=0;j<50;j++)
            printf("%d",chk_d[i][j][1]);
        printf("\n");
    } 
    */
    int dx = x, dy = y, dori = dest_orientation, ccc = 0;
    /*
    if (dori == 5 || dori == 6){
        if(chk_d[dx][dy][dest_orientation][0] == -1) {
            dori += 2;
            if(chk_d[dx][dy][dori][0] == -1) {
                return 0;
            }
       }
    }else{
        if(chk_d[dx][dy][dest_orientation][0] == -1)
            return 0;

    }

    if (dest_orientation == 5 || dest_orientation == 6){
        dest_orientation -= 4;
        dori -= 4;
    }
    */

    if(chk_d[dx][dy][dest_orientation][0] == -1) {
        //dori += 2;
        if(chk_d[dx][dy][dori+2][0] == -1) {
            return 0;
        }
        else
            dori+=2;
    }

    /*  print part  */
    
    FILE *f;
    if (path_print == 1){
        f = fopen(FILE_PATH,"a");//"../routing/path_list"
        fprintf(f, "%d %d %d\n", type_width, type_height, type_bump);
    }
    while(dx >= 0 && _print == 1) { //chk_d[dx][dy][dori][0] != dx && chk_d[dx][dy][dori][1] != dy && 
        printf("x: %d   y: %d   ori: %d         ---- %d\n", dx, dy, dori, ++ccc);
        if (path_print == 1){
            fprintf(f, "%d %d %d\n", dx, dy, dori);
        }
        int tx, ty, tori;
        tx = chk_d[dx][dy][dori][0];
        ty = chk_d[dx][dy][dori][1];
        tori = chk_d[dx][dy][dori][2];
        if(tx == dx && ty == dy || tx == x && ty == y)break;
        dx = tx;
        dy = ty;
        dori = tori;
    }
    while(dx >= 0 && _print == 0) { //chk_d[dx][dy][dori][0] != dx && chk_d[dx][dy][dori][1] != dy && 
        if (path_print == 1){
            fprintf(f, "%d %d %d\n", dx, dy, dori);
        }
        int tx, ty, tori;
        tx = chk_d[dx][dy][dori][0];
        ty = chk_d[dx][dy][dori][1];
        tori = chk_d[dx][dy][dori][2];
        if(tx == dx && ty == dy || tx == x && ty == y)break;
        dx = tx;
        dy = ty;
        dori = tori;
    }
    if (path_print == 1){
        //fprintf(f, "-1\n");
        fclose(f);
    }
    /*
    for(i=0;i<50;i++) {
        for(j=0;j<50;j++) {
            bool xxx = 0;
            for(k=0;k<4;k++) {
                printf("%d %d  ",chk_d[i][j][k][0], chk_d[i][j][k][1]);
            }
            printf("  ");
        }
        printf("\n");
    }*/
    int temp = 0;
    if (chk_d[x][y][dest_orientation][0] >= 0 || chk_d[x][y][dest_orientation+2][0] >= 0)
        temp = 1;
    return temp;//chk_d[x][y][dest_orientation][0] >= 0;
}

static PyObject* graph_init(PyObject *self, PyObject *args)
{
    Py_Initialize();
    PyArrayObject *input=NULL;
    int i, j, k, x, y, z, temparg1, temparg2, temparg3, temparg4;
    if (!PyArg_ParseTuple(args, "iiiiiO!",&temparg1, &temparg2, &temparg3, &temparg4, &type_bump, &PyArray_Type, &input)) return NULL;
    x = input->dimensions[0];
    y = input->dimensions[1];
    grid_height = y;
    grid_width = x;
    type_width = temparg1;
    type_height = temparg2;
    type_minR = temparg3;
    //type_radius = type_minR;
    type_radius = temparg4;
    //printf("minR:%d\n",type_minR);
    type_inner_r = temparg3;
    type_outer_r = temparg3 + type_width;
    //printf("bump %d\n",type_bump);
    small_r_sqr = lsqr(type_radius - type_width);
    large_r_sqr = lsqr(type_radius) + lsqr(type_bump);
    large_r_sqr2 = lsqr(type_radius) + lsqr(type_height - type_bump);
    type_minR = sqrt(large_r_sqr2) + 0.9999;

    //printf("type minR - %d\ntype radius - %d\n",type_minR, type_radius);

    //  printf("%d, %d\n",type_width, type_height);
    npy_intp Dims[2];
    Dims[0] = x;
    Dims[1] = y;
    for(i=0;i<x;i++){
        for(j=0;j<y;j++)
            grid[i][j] = *(double*)(input->data + i*input->strides[0] + j*input->strides[1]);//*(int*)이 안되면 *(double*)
    }

    /*
    printf("income grid\n");
    bool c[105];
    for(i=0;i<x;i++) {
        for(j=0;j<y;j++) {
            printf("%d    ",grid[i][j]);
        }
        printf("\n");
    }
    printf("check vertices and curves\n");
    */

    FILE *f;
    f = fopen(FILE_PATH,"w");//"../routing/path_list"
    fprintf(f,"");
    fclose(f);

    init();
    /*
    printf("%d, %d\n%d, %d\n", vertex[30][20][0], vertex[30][20][1],curve[50][79][5][0],curve[50][79][5][1]);
    printf("end init\n");
    */

    /*
    PyObject *res;
    npy_intp verDim[3] = {grid_width, grid_height, 2};
    res = PyArray_SimpleNew(3, verDim, NPY_INT);
    int *p = (double *) PyArray_DATA(res);
    for (i = 0; i < x; i++) {
        memcpy(p, vertex[i], sizeof(int) * (y + 2));
        p += y+2;
    }
    return Py_BuildValue("O", res);
    */
    /*
    for (i=0;i<50;i++){
        for (j=0; j<50;j++){
            for(k=0;k<8;k++){
                printf("%d %d | ",curve[i][j][k][0], curve[i][j][k][1]);
            }
        }
        printf("\n");
    }
    */
        /*
    printf("\n!\n");
    for(i=0;i<50;i++) {
    for(j=0;j<50;j++) {
        printf("%d ",vertex[i][j][0]);
    }
    printf("\n");
    }
    for(i=0;i<50;i++) {
    for(j=0;j<50;j++) {
        printf("%d ",vertex[i][j][1]);
    }
    printf("\n");
    }
    */

    PyObject *pyVertex = NULL, *pyCurve = NULL;
    Py_Initialize();

    npy_intp verDim[3], curDim[4];
    verDim[0] = grid_width;
    verDim[1] = grid_height;
    verDim[2] = 2;

    curDim[0] = grid_width;
    curDim[1] = grid_height;
    curDim[2] = 8;
    curDim[3] = 2;


    //sleep(3);
    pyVertex = PyArray_SimpleNew(3, verDim, NPY_INT);
    int *pVer = (double *) PyArray_DATA(pyVertex);
    
    for(i=0;i<grid_width;i++){
        for(j=0;j<grid_height;j++) {
                memcpy(pVer,vertex[i][j],sizeof(int)*2);
                pVer += 2;
            
        }
    }

    pyCurve = PyArray_SimpleNew(4, curDim, NPY_INT);
    int *pCur = (double *) PyArray_DATA(pyCurve);

    for(i=0;i<grid_width;i++){
        for(j=0;j<grid_height;j++) {
            for(k=0;k<8;k++) {
                memcpy(pCur,curve[i][j][k],sizeof(int)*2);
                pCur += 2;
            }
        }
    }

    //free(curve);
    //free(vertex);

    PyObject *re1 = Py_BuildValue("OO",pyVertex,pyCurve);

    Py_DECREF(pyVertex);
    Py_DECREF(pyCurve);

    return re1;//Py_BuildValue("OO",pyVertex,pyCurve);


    /*
    int a[5][4][3][2];
    int di[4] = {5,4,3,2};
    PyObject *r;
    r = PyArray_SimpleNew(4, di, NPY_INT);
    int *p = (double *) PyArray_DATA(r);
    int l;
    for(i=0;i<5;i++)
        for(j=0;j<4;j++)
            for(k=0;k<3;k++) {
                for(l=0;l<2;l++) a[i][j][k][l] = i+j+k+l;
                memcpy(p,a[i][j][k],sizeof(int) * 2);
                p += 2;
            }
    return Py_BuildValue("O",r);*/
    //  double out = 0;
    //return Py_BuildValue("O", res);
    //    return Py_BuildValue("f",out);
}

static PyObject* graph_update(PyObject *self, PyObject *args) {
    PyArrayObject *input=NULL, *input2=NULL, *input3=NULL;
    int i, j, k, p, x, y, z, temparg1, temparg2, temparg3;


    double out = 0;
    int s_x,s_y,e_x,e_y;
    if (!PyArg_ParseTuple(args, "iiiiiiiiOO!",&s_x, &s_y, &e_x, &e_y, &temparg1, &temparg2, &temparg3, &type_bump, &input, &PyArray_Type, &input2)) return NULL;
    x = input->dimensions[0];
    y = input->dimensions[1];
    grid_height = y;
    grid_width = x;
    type_width = temparg1;
    type_height = temparg2;
    //type_minR = temparg3;
    type_radius = temparg3;
    //  printf("%d, %d\n",type_width, type_height);

    small_r_sqr = lsqr(type_radius - type_width);
    large_r_sqr = lsqr(type_radius) + lsqr(type_bump);
    large_r_sqr2 = lsqr(type_radius) + lsqr(type_height - type_bump);
    type_minR = sqrt(large_r_sqr2) + 0.9999;

    int dest_orientation;
    if(e_x - s_x > e_y - s_y)
        dest_orientation = 1;
    else
        dest_orientation = 0;
    if (type_height - type_width == 2){
        FILE *f;
        f = fopen(FILE_PATH,"a");//"../routing/path_list"
        fprintf(f, "%d %d %d %d\n", s_x, s_y, e_x, e_y);
        fclose(f);
    }   
    npy_intp verDim[3], curDim[4];

    verDim[0] = grid_width;
    verDim[1] = grid_height;
    verDim[2] = 2;

    curDim[0] = grid_width;
    curDim[1] = grid_height;
    curDim[2] = 8;
    curDim[3] = 2;

    //printf("%d\n", *(double*)(input->data + 30*input->strides[0] + 50*input->strides[1] + 1*input->strides[2]));


    for(i=0;i<x;i++){
        for(j=0;j<y;j++) {
            for(k=0;k<2;k++) {
                vertex[i][j][k] = *(int*)(input->data + i*input->strides[0] + j*input->strides[1] + k*input->strides[2]);//*(int*)이 안되면 *(double*)
            }
        }
        //printf("%d\n",i);
    }
    
    //printf("moving = %d, %d",vertex[30][30][0],vertex[30][30][1]);

    x = input2->dimensions[0];
    y = input2->dimensions[1];
    z = 8;

    for(i=0;i<x;i++){
        for(j=0;j<y;j++) {
            for(k=0;k<z;k++){
                curve[i][j][k][0] = *(int*)(input2->data + i*input2->strides[0] + j*input2->strides[1] + k*input2->strides[2] + 0* input2->strides[3]);//*(int*)이 안되면 *(double*)
                curve[i][j][k][1] = *(int*)(input2->data + i*input2->strides[0] + j*input2->strides[1] + k*input2->strides[2] + 1* input2->strides[3]);//*(int*)이 안되면 *(double*)
            }
    //          printf("%d %d   ", curve[i][j][k][0], curve[i][j][k][1]);
        }
    //      printf("\n\n");
    }

    //  printf("income grid!!!\n");
    //  printf("in update .... start \n");
    // grid 전체를 념겨받음.
      //업데이트 된 grid top-left, bottom-right 좌표정보
    int width = type_width, height = type_height, min_R= type_minR;   //차량의 넓이, 길이, 최소회전반경
    
    int temp;
    if (s_x > e_x){
        temp = s_x;
        s_x = e_x;
        e_x = temp;
    }
    if (s_y > e_y){
        temp = s_y;
        s_y = e_y;
        e_y = temp;
    }

    //printf("sx %d sy %d ex %d ey %d\n",s_x,s_y,e_x,e_y);
    int tmpX = s_x-width+1, tmpY = s_y-height+1;

    if (tmpX < 0)
        tmpX = 0;
    if (tmpY < 0)
        tmpY = 0;

    for(i = tmpX; i <= e_x;i++){
        for (j=tmpY; j <= e_y;j++){
            if(i >= grid_width || j >= grid_height) continue;
            vertex[i][j][0] = not_available;
        }
    }

    tmpX = s_x-height+1;
    tmpY = s_y-width+1;

    if (tmpX < 0)
        tmpX = 0;
    if (tmpY < 0)
        tmpY = 0;

    for(i=tmpX;i <= e_x;i++){
        for(j = tmpY;j <= e_y;j++){
            if(i >= grid_width || j >= grid_height) continue;
            vertex[i][j][1] = not_available;
        }
    }

    for (i=s_x;i<=e_x;i++){
        for (j=s_y;j<=e_y;j++){
            if(i >= grid_width || j >= grid_height) continue;
            grid[i][j] = not_available;
        }
    }
    /*
    printf("\n!\n");
    for(i=0;i<50;i++) {
    for(j=0;j<50;j++) {
        printf("%d ",vertex[j][i][0]);
    }
    printf("\n");
    }
    for(i=0;i<50;i++) {
    for(j=0;j<50;j++) {
        printf("%d ",vertex[j][i][1]);
    }
    printf("\n");
    }*/ 
    /*
    printf("\n!\n");
    for(i=0;i<50;i++) {
        for(j=0;j<50;j++) {
            printf("%d ",vertex[i][j][0]);
        }
        printf("\n");
    }
    printf("\n");
    for(i=0;i<50;i++) {
        for(j=0;j<50;j++) {
            printf("%d ",vertex[i][j][1]);
        }
        printf("\n");
    }
    */

    tmpX = s_x - height - 4;
    tmpY = s_y - height - 4;

    if (tmpX < 0)
        tmpX = 0;
    if (tmpY < 0)
        tmpY = 0;
    


    for(i = tmpX; i <= e_x + height + 4; i++){
        for(j = tmpY; j <= e_y + height + 4; j++){
            if(i >= grid_width || j >= grid_height) continue;
            
            int t1, t2;
            if(vertex[i][j][0] == not_available) {
                for(k=0;k<4;k++)
                    curve[i][j][k][0] = -1, curve[i][j][k][1] = -1;
            }

            else{
                t1 = i + (type_radius) - (type_bump);
                t2 = j + (type_bump) + (type_radius) - (type_width);
                

                if(!down_right(i,j,t1,t2) || vertex[t1][t2][1] == not_available) {
                    curve[i][j][0][0] = -1, curve[i][j][0][1] = -1;                
                }
                t1 = i + (type_width) - (type_radius) - (type_height) + (type_bump);
                t2 = j + (type_bump) + (type_radius) - (type_width);
                
                if(!down_left(i,j,t1,t2) || vertex[t1][t2][1] == not_available) {
                    curve[i][j][1][0] = -1, curve[i][j][1][1] = -1;    
                }
                t1 = i + (type_radius) - (type_bump);
                t2 = j + (type_height) - (type_bump) - (type_radius);
                
                if(!up_right(i,j,t1,t2) || vertex[t1][t2][1] == not_available) {
                    curve[i][j][2][0] = -1, curve[i][j][2][1] = -1; 
                }
                t1 = i + (type_width) - (type_radius) - (type_height) + (type_bump);
                t2 = j + (type_height) - (type_bump) - (type_radius);
                
                if(!up_left(i,j,t1,t2) || vertex[t1][t2][1] == not_available) {
                    curve[i][j][3][0] = -1, curve[i][j][3][1] = -1;                     
                }
            }

            if(vertex[i][j][1] == not_available) {
                for(k=4;k<8;k++)
                    curve[i][j][k][0] = -1, curve[i][j][k][1] = -1;
            }

            else{

                t1 = i + (type_bump) + (type_radius) - (type_width);
                t2 = j + (type_width) - (type_radius) - (type_height) + (type_bump);

                if(!right_up(i,j,t1,t2) || vertex[t1][t2][0] == not_available) {
                    curve[i][j][4][0] = -1, curve[i][j][4][1] = -1;                     
                }
                t1 = i + (type_bump) + (type_radius) - (type_width);
                t2 = j + (type_radius) - (type_bump);

                if(!right_down(i,j,t1,t2) || vertex[t1][t2][0] == not_available) {
                    curve[i][j][5][0] = -1, curve[i][j][5][1] = -1;                     
                }
                t1 = i + (type_height) - (type_bump) - (type_radius);
                t2 = j + (type_width) - (type_radius) - (type_height) + (type_bump);

                if(!left_up(i,j,t1,t2) ||vertex[t1][t2][0] == not_available) {
                    curve[i][j][6][0] = -1, curve[i][j][6][1] = -1;                     
                }
                t1 = i + (type_height) - (type_bump) - (type_radius);
                t2 = j + (type_radius) - (type_bump);

                if(!left_down(i,j,t1,t2) || vertex[t1][t2][0] == not_available) {
                    curve[i][j][7][0] = -1, curve[i][j][7][1] = -1;
                }
            }
        }
    }


    PyObject *pyVertex = NULL, *pyCurve = NULL;
    Py_Initialize();

    pyVertex = PyArray_SimpleNew(3, verDim, NPY_INT);
    int *pVer = (double *) PyArray_DATA(pyVertex);
    
    for(i=0;i<grid_width;i++){
        for(j=0;j<grid_height;j++) {
            memcpy(pVer,vertex[i][j],sizeof(int)*2);
            pVer += 2;
        }
    }

    pyCurve = PyArray_SimpleNew(4, curDim, NPY_INT);
    int *pCur = (double *) PyArray_DATA(pyCurve);

    for(i=0;i<grid_width;i++){
        for(j=0;j<grid_height;j++) {
            for(k=0;k<8;k++) {
                memcpy(pCur,curve[i][j][k],sizeof(int)*2);
                pCur += 2;
            }
        }
    }

    PyObject *re1 = Py_BuildValue("OO",pyVertex,pyCurve);

    Py_DECREF(pyVertex);
    Py_DECREF(pyCurve);

    return re1;


    //return Py_BuildValue("OO",pyVertex,pyCurve);

    /*
    PyObject *res;
    res = PyArray_SimpleNew(2, Dims, NPY_INT);
    int *p = (double *) PyArray_DATA(res);
    for (i = 0; i < x; i++) {
        memcpy(p, grid[i], sizeof(int) * y);
        p += y;
    }
    return Py_BuildValue("O", res);
    */
}

static PyObject* graph_path(PyObject *self, PyObject *args)
{
    PyArrayObject *input=NULL, *input2=NULL;
    int i, j, k, p, x, y, z, temparg1, temparg2, temparg3, _print;
    double out = 0;
    int s_x,s_y,e_x,e_y, ent_x, ent_y, ent_w, ent_h;
    if (!PyArg_ParseTuple(args, "iiiiiiiiiiiiiiOO!",&s_x, &s_y, &e_x, &e_y, &ent_x, &ent_y, &ent_w, &ent_h, &temparg1, &temparg2, &temparg3, &type_bump, &path_print, &_print, &input, &PyArray_Type, &input2)) return NULL;
    x = input->dimensions[0];
    y = input->dimensions[1];
    z = 2;

    grid_height = y;
    grid_width = x;

    type_width = temparg1;
    type_height = temparg2;
    type_minR = temparg3;

    //  printf("%d %d\n",x,y);
    if(ent_y == 0)
        ent_orientation = 2;
    else if(ent_y + ent_h == y)
        ent_orientation = 0;
    else if(ent_x == 0)
        ent_orientation = 1;
    else if(ent_x + ent_w == x)
        ent_orientation = 3;

    //else
    //    ent_orientation = 1;

    int dest_orientation;
    if(e_x - s_x + 1 == type_width){
        dest_orientation = 0;
        /*
        if (s_x + type_height == grid_width - 1)
            dest_orientation = 3;
        else if (s_x == 1)
            dest_orientation = 1;
        else
            dest_orientation = 5;
        */
    }
    else{
        dest_orientation = 1;
        /*
        if (s_y == 1)
            dest_orientation = 2;
        else if (s_y + type_height == grid_height  - 1)
            dest_orientation = 0;
        else
            dest_orientation = 6;
        */
    }
    

    //  printf("%d, %d\n",type_width, type_height);

    npy_intp Dims[3];
    Dims[0] = x;
    Dims[1] = y;
    Dims[2] = z;
    //printf("%d, %d, %d\n",x,y,z);
    //printf("%d\n", *(int*)(input->data + 30*input->strides[0] + 50*input->strides[1] + 1*input->strides[2]));
    for(i=0;i<x;i++){
        for(j=0;j<y;j++) {
            for(k=0;k<z;k++) {
                vertex[i][j][k] = *(int*)(input->data + i*input->strides[0] + j*input->strides[1] + k*input->strides[2]);//*(int*)이 안되면 *(double*)
            }
        }
    }

    //printf("moving = %d, %d",vertex[30][30][0],vertex[30][30][1]);

    x = input2->dimensions[0];
    y = input2->dimensions[1];
    z = 8;

    Dims[0] = x;
    Dims[1] = y;
    Dims[2] = z;

    for(i=0;i<x;i++){
        for(j=0;j<y;j++) {
            for(k=0;k<z;k++){
                curve[i][j][k][0] = *(int*)(input2->data + i*input2->strides[0] + j*input2->strides[1] + k*input2->strides[2] + 0* input2->strides[3]);//*(int*)이 안되면 *(double*)
                curve[i][j][k][1] = *(int*)(input2->data + i*input2->strides[0] + j*input2->strides[1] + k*input2->strides[2] + 1* input2->strides[3]);//*(int*)이 안되면 *(double*)
            }   //printf("%d %d   ", curve[i][j][k][0], curve[i][j][k][1]);
        }
    //      printf("\n\n");
    }
    
    //printf("income grid!!!!!\n"); 
    int re=0;
    //_print =1;
    for(i=0;i<MAX;i++)
        for(j=0;j<MAX;j++)
            for(k=0;k<4;k++)
                for(p=0;p<2;p++)
                chk_d[i][j][k][p] = -1;
    for(i=ent_x;i<ent_x+ent_w;i++){
        for(j=ent_y;j<ent_y + ent_h;j++){
            re = find_path(s_x, s_y, i, j, dest_orientation, _print);
            if (re==1)
                break;
        }
        if (re==1)
            break;
    }
    //printf("re:%d\n",re);
    //printf("%d, %d",vertex[30][30][0],vertex[30][30][1]);
    return Py_BuildValue("i", re);
}

static PyObject* path_list(PyObject *self, PyObject *args)
{
    PyArrayObject *input=NULL, *input2=NULL;
    int i, j, k, p, x, y, z, temparg1, temparg2, temparg3, _print;
    double out = 0;
    int s_x,s_y,e_x,e_y, ent_x, ent_y, ent_w, ent_h;
    if (!PyArg_ParseTuple(args, "iiiiiiiiOO!", &ent_x, &ent_y, &ent_w, &ent_h, &temparg1, &temparg2, &temparg3, &_print, &input,&PyArray_Type, &input2)) return NULL;
    x = input->dimensions[0];
    y = input->dimensions[1];
    z = 2;
    //  printf("%d %d\n",x,y);
    if(ent_y == 0||ent_y + ent_h == y)
        ent_orientation = 0;
    
    else
        ent_orientation = 1;


    int dest_orientation = 1;
    /*
    if(e_x - s_x + 1 != type_width)
        dest_orientation = 1;
    else
        dest_orientation = 0;
    */
    grid_height = y;
    grid_width = x;

    type_width = temparg1;
    type_height = temparg2;
    type_minR = temparg3;

    //  printf("%d, %d\n",type_width, type_height);

    npy_intp Dims[3];
    Dims[0] = x;
    Dims[1] = y;
    Dims[2] = z;
    //printf("%d, %d, %d\n",x,y,z);
    //printf("%d\n", *(int*)(input->data + 30*input->strides[0] + 50*input->strides[1] + 1*input->strides[2]));
    for(i=0;i<x;i++){
        for(j=0;j<y;j++) {
            for(k=0;k<z;k++) {
                vertex[i][j][k] = *(int*)(input->data + i*input->strides[0] + j*input->strides[1] + k*input->strides[2]);//*(int*)이 안되면 *(double*)
            }
        }
    }
    //printf("moving = %d, %d",vertex[30][30][0],vertex[30][30][1]);

    x = input2->dimensions[0];
    y = input2->dimensions[1];
    z = 8;

    Dims[0] = x;
    Dims[1] = y;
    Dims[2] = z;

    for(i=0;i<x;i++){
        for(j=0;j<y;j++) {
            for(k=0;k<z;k++)
                curve[i][j][k][0] = *(int*)(input2->data + i*input2->strides[0] + j*input2->strides[1] + k*input2->strides[2] + 0* input2->strides[3]);//*(int*)이 안되면 *(double*)
                curve[i][j][k][1] = *(int*)(input2->data + i*input2->strides[0] + j*input2->strides[1] + k*input2->strides[2] + 1* input2->strides[3]);//*(int*)이 안되면 *(double*)
    //          printf("%d %d   ", curve[i][j][k][0], curve[i][j][k][1]);
        }
    //      printf("\n\n");
    }

    //printf("income grid!!!!!\n"); 
    int re=0;
    //_print =1;
    for(i=0;i<MAX;i++)
        for(j=0;j<MAX;j++)
            for(k=0;k<4;k++)
                for(p=0;p<2;p++)
                chk_d[i][j][k][p] = -1;
    for(i=ent_x;i<ent_x+ent_w;i++){
        for(j=ent_y;j<ent_y + ent_h;j++){
            re = find_path(s_x, s_y, i, j, dest_orientation, _print);
            //if (re==1)
            //    break;
        }
        //if (re==1)
        //    break;
    }
    
    PyObject *pyList = NULL;
    Py_Initialize();

    npy_intp LstDim[4];

    LstDim[0] = grid_width;
    LstDim[1] = grid_height;
    LstDim[2] = 4;
    LstDim[3] = 4;

    pyList = PyArray_SimpleNew(4, LstDim, NPY_INT);
    int *pLst = (double *) PyArray_DATA(pyList);
    
    for(i=0;i<grid_width;i++){
        for(j=0;j<grid_height;j++) {
            for(k=0;k<4;k++){
                memcpy(pLst,chk_d[i][j][k],sizeof(int)*4);
               pLst += 4;
            }
        }
    }

    return Py_BuildValue("O",pyList);
}

static PyMethodDef graph_funcs[] = {

        {"path_list", path_list, METH_VARARGS, "path list retrun, return list."},

        {"path_chk", graph_path, METH_VARARGS, "path find, return true or false."},

        {"update", graph_update, METH_VARARGS, "map update, vertex, curve update."},

        {"init", graph_init, METH_VARARGS, "Calculate the standard deviation pixelwise."},

        {NULL}
};


void initgraph_m(void)//inithelloworld(void)
{
    Py_InitModule3("graph_m", graph_funcs, "Extension module example!");
    import_array();
} 


bool check_down_right(int top_x, int top_y, int inner_r, int outer_r, int width, int height) {

    int i,j;    
    int param_x = top_x + width / 2;
    int param_y = top_y + height / 2;
    int x = param_x + (outer_r + inner_r)/2;
    int y = param_y;
    //printf("y: %d inner_r: %d\n",y,inner_r);
    for(i=y;i<y+inner_r;i++) {

        int inner_x = x - (int)(floor(sqrt(inner_r*inner_r - (y-i)*(y-i))));
        int outer_x = x - (int)(ceil(sqrt(outer_r*outer_r - (y-i)*(y-i))));

        for(j=outer_x; j<=inner_x; j++)
            //printf("%d %d | ",j,i);
            if(grid[j][i] == not_available){
                //printf("%d, %d, = %d | ",j,i,grid[j][i]);
                return 0;
            }
    }

    for(i=y+inner_r;i<=y+outer_r;i++) {

        int outer_x = x - (int)(ceil(sqrt(outer_r*outer_r-(y-i)*(y-i))));
        for(j=outer_x;j<=x;j++)
            if(grid[j][i] == not_available){
                //printf("%d, %d, = %d | ",j,i,grid[j][i]);
                return 0;
            }
    }
    //rintf("done");
    return 1;
}

bool check_up_right(int top_x, int top_y, int inner_r, int outer_r, int width, int height) {
 
    int i,j;    
    int param_x = top_x + width / 2;
    int param_y = top_y + height / 2;
    int x = param_x + (outer_r + inner_r)/2;
    int y = param_y;

    for(i=y;i>y-inner_r;i--) {
        int inner_x = x - (int)(floor(sqrt(inner_r*inner_r - (y-i)*(y-i))));
        int outer_x = x - (int)(ceil(sqrt(outer_r*outer_r - (y-i)*(y-i))));
        for(j=outer_x; j<=inner_x; j++)
            if(grid[j][i] == not_available)
                return 0;
    }
    for(i=y-inner_r;i>=y-outer_r;i--) {
        int outer_x = x - (int)(ceil(sqrt(outer_r*outer_r-(y-i)*(y-i))));
        for(j=outer_x;j<=x;j++)
            if(grid[j][i] == not_available)
                return 0;
    }
    return 1;
}

bool check_down_left(int top_x, int top_y, int inner_r, int outer_r, int width, int height) {
    int i,j;    
    int param_x = top_x + width / 2;
    int param_y = top_y + height / 2;
    int x = param_x - (outer_r + inner_r)/2;
    int y = param_y;
    for(i=y;i<y+inner_r;i++) {
        int inner_x = x + (int)(floor(sqrt(inner_r*inner_r - (y-i)*(y-i))));
        int outer_x = x + (int)(ceil(sqrt(outer_r*outer_r - (y-i)*(y-i))));
        for(j=inner_x; j<=outer_x; j++)
            if(grid[j][i] == not_available)
                return 0;
    }
    for(i=y+inner_r;i<=y+outer_r;i++) {
        int outer_x = x + (int)(ceil(sqrt(outer_r*outer_r-(y-i)*(y-i))));
        for(j=x;j<=outer_x;j++)
            if(grid[j][i] == not_available)
                return 0;
    }
    return 1;
}

bool check_up_left(int top_x, int top_y, int inner_r, int outer_r, int width, int height) {
    int i,j;    
    int param_x = top_x + width / 2;
    int param_y = top_y + height / 2;
    int x = param_x - (outer_r + inner_r)/2;
    int y = param_y;
    for(i=y;i>y-inner_r;i--) {
        int inner_x = x + (int)(floor(sqrt(inner_r*inner_r - (y-i)*(y-i))));
        int outer_x = x + (int)(ceil(sqrt(outer_r*outer_r - (y-i)*(y-i))));
        for(j=inner_x; j<=outer_x; j++)
            if(grid[j][i] == not_available)
                return 0;
    }
    for(i=y-inner_r;i>=y-outer_r;i--) {
        int outer_x = x + (int)(ceil(sqrt(outer_r*outer_r-(y-i)*(y-i))));
        for(j=x;j<=outer_x;j++)
            if(grid[j][i] == not_available)
                return 0;
    }
    return 1;
}

bool check_left_up(int top_x, int top_y, int inner_r, int outer_r, int width, int height) {
    int i,j;    
    int param_x = top_x + height / 2;
    int param_y = top_y + width / 2;
    int x = param_x;
    int y = param_y - (outer_r + inner_r)/2;
    for(i=y;i<y+inner_r;i++) {
        int inner_x = x - (int)(floor(sqrt(inner_r*inner_r - (y-i)*(y-i))));
        int outer_x = x - (int)(ceil(sqrt(outer_r*outer_r - (y-i)*(y-i))));
        for(j=outer_x; j<=inner_x; j++)
            if(grid[j][i] == not_available)
                return 0;
    }
    for(i=y+inner_r;i<=y+outer_r;i++) {
        int outer_x = x - (int)(ceil(sqrt(outer_r*outer_r-(y-i)*(y-i))));
        for(j=outer_x;j<=x;j++)
            if(grid[j][i] == not_available)
                return 0;
    }
    return 1;
}

bool check_right_up(int top_x, int top_y, int inner_r, int outer_r, int width, int height) {
    int i,j;    
    int param_x = top_x + height / 2;
    int param_y = top_y + width / 2;
    int x = param_x;
    int y = param_y - (outer_r + inner_r)/2;
    for(i=y;i<y+inner_r;i++) {
        int inner_x = x + (int)(floor(sqrt(inner_r*inner_r - (y-i)*(y-i))));
        int outer_x = x + (int)(ceil(sqrt(outer_r*outer_r - (y-i)*(y-i))));
        for(j=inner_x; j<=outer_x; j++)
            if(grid[j][i] == not_available)
                return 0;
    }
    for(i=y+inner_r;i<=y+outer_r;i++) {
        int outer_x = x + (int)(ceil(sqrt(outer_r*outer_r-(y-i)*(y-i))));
        for(j=x;j<=outer_x;j++)
            if(grid[j][i] == not_available)
                return 0;
    }
    return 1;
}

bool check_left_down(int top_x, int top_y, int inner_r, int outer_r, int width, int height) {
    int i,j;    
    int param_x = top_x + height / 2;
    int param_y = top_y + width / 2;
    int x = param_x;
    int y = param_y + (outer_r + inner_r)/2;
    for(i = y; i > y-inner_r; i--) {
        int inner_x = x - (int)(floor(sqrt(inner_r*inner_r - (y-i)*(y-i))));
        int outer_x = x - (int)(ceil(sqrt(outer_r*outer_r - (y-i)*(y-i))));
        for(j=outer_x; j<=inner_x; j++)
            if(grid[j][i] == not_available)
                return 0;
    }
    for(i = y - inner_r; i >= y - outer_r; i--) {
        int outer_x = x - (int)(ceil(sqrt(outer_r*outer_r-(y-i)*(y-i))));
        for(j=outer_x;j<=x;j++)
            if(grid[j][i] == not_available)
                return 0;
    }
    return 1;
}

bool check_right_down(int top_x, int top_y, int inner_r, int outer_r, int width, int height) {
    int i,j;    
    int param_x = top_x + height / 2;
    int param_y = top_y + width / 2;
    int x = param_x;
    int y = param_y + (outer_r + inner_r)/2;
    for(i=y;i>y-inner_r;i--) {
        int inner_x = x - (int)(ceil(sqrt(inner_r*inner_r - (y-i)*(y-i))));
        int outer_x = x - (int)(floor(sqrt(outer_r*outer_r - (y-i)*(y-i))));
        for(j=inner_x; j<=outer_x; j++)
            if(grid[j][i] == not_available)
                return 0;
    }
    for(i=y-inner_r;i>=y-outer_r;i--) {
        int outer_x = x + (int)(ceil(sqrt(outer_r*outer_r-(y-i)*(y-i))));
        for(j=x;j<=outer_x;j++)
            if(grid[j][i] == not_available)
                return 0;
    }
    return 1;
}