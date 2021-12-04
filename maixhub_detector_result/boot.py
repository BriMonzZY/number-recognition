# object detector boot.py
# generated by maixhub.com

import sensor, image, lcd, time
import KPU as kpu
import gc, sys

def lcd_show_except(e):
    import uio
    err_str = uio.StringIO()
    sys.print_exception(e, err_str)
    err_str = err_str.getvalue()
    img = image.Image(size=(224,224))
    img.draw_string(0, 10, err_str, scale=1, color=(0xff,0x00,0x00))
    lcd.display(img)

def main(anchors, labels = None, model_addr=0x300000, sensor_window=(224, 224), lcd_rotation=0, sensor_hmirror=True, sensor_vflip=True):
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_windowing(sensor_window)
    sensor.set_hmirror(sensor_hmirror)
    sensor.set_vflip(sensor_vflip)
    sensor.run(1)

    lcd.init(type=1)
    lcd.rotation(lcd_rotation)
    lcd.clear(lcd.WHITE)

    #if not labels:
        #with open('labels.txt','r') as f:
            #exec(f.read())
    #if not labels:
        #print("no labels.txt")
        #img = image.Image(size=(320, 240))
        #img.draw_string(90, 110, "no labels.txt", color=(255, 0, 0), scale=2)
        #lcd.display(img)
        #return 1
    try:
        img = image.Image("startup.jpg")
        lcd.display(img)
    except Exception:
        img = image.Image(size=(320, 240))
        img.draw_string(90, 110, "loading model...", color=(255, 255, 255), scale=2)
        print("loading..")
        lcd.display(img)

    try:
        task = None


        task = kpu.load(model_addr)
        # task = kpu.load(0x300000)
        kpu.init_yolo2(task, 0.5, 0.3, 5, anchors) # threshold:[0,1], nms_value: [0, 1]

        clock = time.clock()

        while(True):
            clock.tick()
            img = sensor.snapshot()
            t = time.ticks_ms()
            objects = kpu.run_yolo2(task, img)
            t = time.ticks_ms() - t
            if objects:
                for obj in objects:
                    pos = obj.rect()
                    img.draw_rectangle(pos)
                    img.draw_string(pos[0], pos[1], "%s : %.2f" %(labels[obj.classid()], obj.value()), scale=2, color=(255, 0, 0))
            img.draw_string(0, 200, "fps:%d" %(clock.fps()), scale=2, color=(255, 0, 0))
            lcd.display(img)
    except Exception as e:
        raise e
        print("faile")
    finally:
        if not task is None:
            kpu.deinit(task)


if __name__ == "__main__":
    try:
        labels = ["1", "2", "3", "4", "5", "6", "7", "8"]
        anchors = [2.1875, 2.625, 1.78125, 1.5625, 1.9062499999999998, 2.09375, 1.5625, 1.8125000000000002, 1.375, 1.4375]
        # main(anchors = anchors, labels=labels, model_addr=0x300000, lcd_rotation=0)
        main(anchors = anchors, labels=labels, model_addr=0x300000)
    except Exception as e:
        sys.print_exception(e)
        lcd_show_except(e)
    finally:
        gc.collect()
