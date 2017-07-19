#include <python2.7/Python.h>
#include <numpy/arrayobject.h>
#include <math.h>
#include <stdbool.h>

#define not_available 0
#define available 1

int grid[2500][2500];
int vertex[2500][2500][2];
int acc[2500][2500];
//int curveDest[8][2500][2500][2];
bool curve[2500][2500][8][2];
int grid_width=600, grid_height=600;
int type_width, type_height, type_inner_r, type_outer_r, type_minR;

bool check_down_right(int top_x, int top_y, int inner_r, int outer_r, int width, int height) {
    int i,j;    
    int param_x = top_x + width / 2;
    int param_y = top_y + height / 2;
    
    int x = param_x + (outer_r + inner_r)/2;
    int y = param_y;

    for(i=y;i<y+inner_r;i++) {
        int inner_x = x - (int)(floor(sqrt(inner_r*inner_r - (y-i)*(y-i))));
        int outer_x = x - (int)(floor(sqrt(outer_r*outer_r - (y-i)*(y-i))));
        for(j=outer_x; j<=inner_x; j++)
            if(grid[j][i] == not_available)
                return 0;
    }
    for(i=y+inner_r;i<=y+outer_r;i++) {
        int outer_x = x - (int)(floor(sqrt(outer_r*outer_r-(y-i)*(y-i))));
        for(j=outer_x;j<=x;j++)
            if(grid[j][i] == not_available)
                return 0;
    }
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
        int outer_x = x - (int)(floor(sqrt(outer_r*outer_r - (y-i)*(y-i))));
        for(j=outer_x; j<=inner_x; j++)
            if(grid[j][i] == not_available)
                return 0;
    }
    for(i=y-inner_r;i>=y-outer_r;i--) {
        int outer_x = x - (int)(floor(sqrt(outer_r*outer_r-(y-i)*(y-i))));
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
        int outer_x = x + (int)(floor(sqrt(outer_r*outer_r - (y-i)*(y-i))));
        for(j=inner_x; j<=outer_x; j++)
            if(grid[j][i] == not_available)
                return 0;
    }
    for(i=y+inner_r;i<=y+outer_r;i++) {
        int outer_x = x + (int)(floor(sqrt(outer_r*outer_r-(y-i)*(y-i))));
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
        int outer_x = x + (int)(floor(sqrt(outer_r*outer_r - (y-i)*(y-i))));
        for(j=inner_x; j<=outer_x; j++)
            if(grid[j][i] == not_available)
                return 0;
    }
    for(i=y-inner_r;i>=y-outer_r;i--) {
        int outer_x = x + (int)(floor(sqrt(outer_r*outer_r-(y-i)*(y-i))));
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
        int outer_x = x - (int)(floor(sqrt(outer_r*outer_r - (y-i)*(y-i))));
        for(j=outer_x; j<=inner_x; j++)
            if(grid[j][i] == not_available)
                return 0;
    }
    for(i=y+inner_r;i<=y+outer_r;i++) {
        int outer_x = x - (int)(floor(sqrt(outer_r*outer_r-(y-i)*(y-i))));
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
        int outer_x = x + (int)(floor(sqrt(outer_r*outer_r - (y-i)*(y-i))));
        for(j=inner_x; j<=outer_x; j++)
            if(grid[j][i] == not_available)
                return 0;
    }
    for(i=y+inner_r;i<=y+outer_r;i++) {
        int outer_x = x + (int)(floor(sqrt(outer_r*outer_r-(y-i)*(y-i))));
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
        int outer_x = x - (int)(floor(sqrt(outer_r*outer_r - (y-i)*(y-i))));
        for(j=outer_x; j<=inner_x; j++)
            if(grid[j][i] == not_available)
                return 0;
    }
    for(i = y - inner_r; i >= y - outer_r; i--) {
        int outer_x = x - (int)(floor(sqrt(outer_r*outer_r-(y-i)*(y-i))));
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
        int inner_x = x - (int)(floor(sqrt(inner_r*inner_r - (y-i)*(y-i))));
        int outer_x = x - (int)(floor(sqrt(outer_r*outer_r - (y-i)*(y-i))));
        for(j=inner_x; j<=outer_x; j++)
            if(grid[j][i] == not_available)
                return 0;
    }
    for(i=y-inner_r;i>=y-outer_r;i--) {
        int outer_x = x + (int)(floor(sqrt(outer_r*outer_r-(y-i)*(y-i))));
        for(j=x;j<=outer_x;j++)
            if(grid[j][i] == not_available)
                return 0;
    }
    return 1;
}

//int grid_width=600, grid_height=600;
//int type_width, type_height, type_inner_r, type_outer_r, type_minR;

void init() {
    int i,j,l,p;
    for(i=0;i<grid_width;i++) {
        for(j=0;j<grid_height;j++)
            if(i && j)
                acc[i][j] = grid[i-1][j] + grid[i][j-1] - grid[i-1][j-1];
    }
    for(i=0;i<grid_width;i++) {
        for(j=0;j<grid_height;j++) {
            vertex[i][j][0] = not_available;    
            vertex[i][j][1] = not_available;    
            int t1 = i-type_width;
            int t2 = j-type_height; 
            if(t1 > 0 && t2 > 0)
                if(acc[i][j] - acc[t1-1][j] - acc[i][t2-1] + acc[t1-1][t2-1] == 0)
                    vertex[i][j][0] = available;
            t1 = i-type_height;
            t2 = j-type_width; 
            if(t1 > 0 && t2 > 0)
                if(acc[i][j] - acc[t1-1][j] - acc[i][t2-1] + acc[t1-1][t2-1] == 0)
                    vertex[i][j][1] = available;
        }//(int top_x, int top_y, int inner_r, int outer_r, int width, int height)
    }
    for(i=0;i<grid_width;i++) {
        for(j=0;j<grid_height;j++) {
            int t1, t2;
            if(vertex[i][j][0] == available) {
                t1 = i + type_minR, t2 = j + type_minR - type_width;
                if(t1 >= 0 && t2 >= 0 && t1 < grid_width && t2 < grid_height)
                    if(vertex[t1][t2][1])
                        if(check_down_right(i, j, type_inner_r, type_outer_r, type_width, type_height))
                            curve[i][j][0][0] = t1, curve[i][j][0][1] = t2;
                t1 = i - type_minR + type_width + type_height, t2 = j + type_minR - type_width;
                if(t1 >= 0 && t2 >= 0 && t1 < grid_width && t2 < grid_height)
                    if(vertex[t1][t2][1])
                        if(check_down_left(i, j, type_inner_r, type_outer_r, type_width, type_height))
                            curve[i][j][1][0] = t1, curve[i][j][1][1] = t2;
                t1 = i + type_minR - type_height, t2 = j + type_minR;
                if(t1 >= 0 && t2 >= 0 && t1 < grid_width && t2 < grid_height)
                    if(vertex[t1][t2][1])
                        if(check_up_right(i, j, type_inner_r, type_outer_r, type_width, type_height))
                            curve[i][j][2][0] = t1, curve[i][j][2][1] = t2;
                t1 = i - type_minR + type_width - type_height, t2 = j + type_minR;
                if(t1 >= 0 && t2 >= 0 && t1 < grid_width && t2 < grid_height)
                    if(vertex[t1][t2][1])
                        if(check_up_left(i, j, type_inner_r, type_outer_r, type_width, type_height))
                            curve[i][j][3][0] = t1, curve[i][j][3][1] = t2;
            }
            if(vertex[i][j][1] == available) {
                t1 = i + type_minR - type_width + type_height, t2 = j + type_minR;
                if(t1 >= 0 && t2 >= 0 && t1 < grid_width && t2 < grid_height)
                    if(vertex[t1][t2][1])
                        if(check_right_up(i, j, type_inner_r, type_outer_r, type_width, type_height))
                            curve[i][j][4][0] = t1, curve[i][j][4][1] = t2;
                t1 = i + type_minR - type_width, t2 = j + type_minR;
                if(t1 >= 0 && t2 >= 0 && t1 < grid_width && t2 < grid_height)
                    if(vertex[t1][t2][1])
                        if(check_right_down(i, j, type_inner_r, type_outer_r, type_width, type_height))
                            curve[i][j][5][0] = t1, curve[i][j][5][1] = t2;
                t1 = i - type_minR, t2 = j + type_minR - type_width;
                if(t1 >= 0 && t2 >= 0 && t1 < grid_width && t2 < grid_height)
                    if(vertex[t1][t2][1])
                        if(check_left_up(i, j, type_inner_r, type_outer_r, type_width, type_height))
                            curve[i][j][6][0] = t1, curve[i][j][6][1] = t2;
                t1 = i - type_minR + type_height, t2 = j + type_minR;
                if(t1 >= 0 && t2 >= 0 && t1 < grid_width && t2 < grid_height)
                    if(vertex[t1][t2][1])
                        if(check_left_down(i, j, type_inner_r, type_outer_r, type_width, type_height))
                            curve[i][j][7][0] = t1, curve[i][j][7][1] = t2;

            }

        }
    }
}

static PyObject*

myexts_std(PyObject *self, PyObject *args)
{
    PyArrayObject *input=NULL;
    int i, j, k, x, y, temparg1, temparg2, temparg3;
    double out = 0;

    if (!PyArg_ParseTuple(args, "iiiO!",&temparg1, &temparg2, &temparg3, &PyArray_Type, &input)) return NULL;
    x = input->dimensions[0];
    y = input->dimensions[1];
    grid_height = y;
    grid_width = x;
    
    type_width = temparg1;
    type_height = temparg2;
    type_minR = temparg3;

    printf("%d, %d\n",type_width, type_height);
    npy_intp Dims[2];
    Dims[0] = x;
    Dims[1] = y;

    for(i=0;i<x;i++){
        for(j=0;j<y;j++)
            grid[i][j] = *(double*)(input->data + i*input->strides[0] + j*input->strides[1]);//*(int*)이 안되면 *(double*)
    }
    printf("income grid\n");
    bool c[105];
    for(i=0;i<x;i++) {
        for(j=0;j<y;j++) {
            printf("%d    ",grid[i][j]);
        }
        printf("\n");
    }

    printf("check vertices and curves\n");

    init();
    /*
    PyObject *res;
    res = PyArray_SimpleNew(2, Dims, NPY_INT);
    int *p = (double *) PyArray_DATA(res);
    for (i = 0; i < x; i++) {
        memcpy(p, grid[i], sizeof(int) * y);
        p += y;
    }
    
    printf("hhh");
    int a[5][4][3][2];
    int idx[4] = {5,4,3,2};
    PyObject *res;
    res = PyArray_SimpleNew(4, idx,NPY_INT);
    int *p = (double *) PyArray_DATA(res);
    int l;
   
    for (i=0;i<5;i++){
        for(j=0;j<4;j++){
            for(k=0;k<3;k++){
                for(l=0;l<2;l++) a[i][j][k][l] = i+j+k+l;
                memcpy(p,a[i][j][k],sizeof(int) * 2);
                p += 2;
            }
        }
    }
    */

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
    return Py_BuildValue("O",r);
    //return Py_BuildValue("O", res);
//    return Py_BuildValue("f",out);
}
my_update(PyObject *self, PyObject *args)
{
    PyArrayObject *input=NULL;
    int i, j, k, x, y, temparg1, temparg2, temparg3;
    double out = 0;
    int s_x,s_y,e_x,e_y;  
    if (!PyArg_ParseTuple(args, "iiiiiiiO!",&s_x, &s_y, &e_x, &e_y, &temparg1, &temparg2, &temparg3, &PyArray_Type, &input)) return NULL;
    x = input->dimensions[0];
    y = input->dimensions[1];

    grid_height = y;
    grid_width = x;
    
    type_width = temparg1;
    type_height = temparg2;
    type_minR = temparg3;

    printf("%d, %d\n",type_width, type_height);
    npy_intp Dims[2];
    Dims[0] = x;
    Dims[1] = y;

    for(i=0;i<x;i++){
        for(j=0;j<y;j++)
            grid[i][j] = *(double*)(input->data + i*input->strides[0] + j*input->strides[1]);//*(int*)이 안되면 *(double*)
    }
    printf("income grid!!!\n");
    bool c[105];
    for(i=0;i<x;i++) {
        for(j=0;j<y;j++) {
            printf("%d    ",grid[i][j]);
        }
        printf("\n");
    }
    printf("in update .... start mimipart \n");
    // grid 전체를 념겨받음.
      //업데이트 된 grid top-left, bottom-right 좌표정보
    int width = type_width, height = type_height, min_R= type_minR;   //차량의 넓이, 길이, 최소회전반경 
    int inner = min_R - width;
    for(int i = s_x-width;i< e_x;i++){
        for (int j=s_y-height; j<e_y;j++){
            vertex[i][j][0] = not_available;
        }
    }
    
    for(int i=s_x-height;i< e_x;i++){
        for(int j = s_y-width;j < e_y;j++){
            vertex[i][j][1] = not_available;
        }
    }

    for(int i = s_x - min_R; i < e_x + min_R;i++){
        for(int j=s_y - min_R;j < e_y - min_R;j++){
            int t1, t2;
            if(vertex[i][j][0] == available) {
                t1 = i + type_minR, t2 = j + type_minR - type_width;
                if(t1 >= 0 && t2 >= 0 && t1 < grid_width && t2 < grid_height)
                    if(vertex[t1][t2][1])
                        if(check_down_right(i, j, type_inner_r, type_outer_r, type_width, type_height))
                            curve[i][j][0][0] = t1, curve[i][j][0][1] = t2;
                t1 = i - type_minR + type_width + type_height, t2 = j + type_minR - type_width;
                if(t1 >= 0 && t2 >= 0 && t1 < grid_width && t2 < grid_height)
                    if(vertex[t1][t2][1])
                        if(check_down_left(i, j, type_inner_r, type_outer_r, type_width, type_height))
                            curve[i][j][1][0] = t1, curve[i][j][1][1] = t2;
                t1 = i + type_minR - type_height, t2 = j + type_minR;
                if(t1 >= 0 && t2 >= 0 && t1 < grid_width && t2 < grid_height)
                    if(vertex[t1][t2][1])
                        if(check_up_right(i, j, type_inner_r, type_outer_r, type_width, type_height))
                            curve[i][j][2][0] = t1, curve[i][j][2][1] = t2;
                t1 = i - type_minR + type_width - type_height, t2 = j + type_minR;
                if(t1 >= 0 && t2 >= 0 && t1 < grid_width && t2 < grid_height)
                    if(vertex[t1][t2][1])
                        if(check_up_left(i, j, type_inner_r, type_outer_r, type_width, type_height))
                            curve[i][j][3][0] = t1, curve[i][j][3][1] = t2;
            }
            if(vertex[i][j][1] == available) {
                t1 = i + type_minR - type_width + type_height, t2 = j + type_minR;
                if(t1 >= 0 && t2 >= 0 && t1 < grid_width && t2 < grid_height)
                    if(vertex[t1][t2][1])
                        if(check_right_up(i, j, type_inner_r, type_outer_r, type_width, type_height))
                            curve[i][j][4][0] = t1, curve[i][j][4][1] = t2;
                t1 = i + type_minR - type_width, t2 = j + type_minR;
                if(t1 >= 0 && t2 >= 0 && t1 < grid_width && t2 < grid_height)
                    if(vertex[t1][t2][1])
                        if(check_right_down(i, j, type_inner_r, type_outer_r, type_width, type_height))
                            curve[i][j][5][0] = t1, curve[i][j][5][1] = t2;
                t1 = i - type_minR, t2 = j + type_minR - type_width;
                if(t1 >= 0 && t2 >= 0 && t1 < grid_width && t2 < grid_height)
                    if(vertex[t1][t2][1])
                        if(check_left_up(i, j, type_inner_r, type_outer_r, type_width, type_height))
                            curve[i][j][6][0] = t1, curve[i][j][6][1] = t2;
                t1 = i - type_minR + type_height, t2 = j + type_minR;
                if(t1 >= 0 && t2 >= 0 && t1 < grid_width && t2 < grid_height)
                    if(vertex[t1][t2][1])
                        if(check_left_down(i, j, type_inner_r, type_outer_r, type_width, type_height))
                            curve[i][j][7][0] = t1, curve[i][j][7][1] = t2;
            }
        }
    }
   PyObject *res;
    res = PyArray_SimpleNew(2, Dims, NPY_INT);
    int *p = (double *) PyArray_DATA(res);
    for (i = 0; i < x; i++) {
        memcpy(p, grid[i], sizeof(int) * y);
        p += y;
    }
    return Py_BuildValue("O", res);
}
static PyMethodDef helloworld_funcs[] = {
        //{"update", my_update, METH_VARARGS, "map update, vertex, curve update."},
        {"mean", myexts_std, METH_VARARGS, "Calculate the standard deviation pixelwise."},
    {NULL}
};

void inithelloworld(void)
{
    Py_InitModule3("helloworld", helloworld_funcs, "Extension module example!");
    import_array();
} 